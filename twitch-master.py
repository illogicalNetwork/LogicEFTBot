import signal
import time
import threading
import math
import os
from typing import Callable, List, Any
from typing import List
from dataclasses import dataclass
from queue import Empty
from multiprocessing import Queue, Process
from twitch import TwitchIrcBot
from bot.database import Database
from bot.config import settings
from bot.log import log

DB: Database = Database.get()
DB_OBSERVER_THREAD = None
DB_OBSERVER_THREAD_LIVE = True
ABORT_STARTUP = False
END_OF_LIFE = -1
TOTAL_SHARDS = 0
SHUTDOWN_INITIATED: threading.Event = threading.Event()


@dataclass
class Shard:
    """
    A shard manages the state for a connection of a certain number of channels.
    The "saturation" of the shard is the number of channels its connected to.

    A shard is considered saturated if it has joined too many channels
    (as defined in settings, "shard_size")
    """

    process: Process
    queue: Queue
    saturation: int = 0

    def is_saturated(self) -> bool:
        """
        Returns true if more channels can be joined on this connection.
        """
        return self.saturation >= int(settings["shard_size"])

    def start(self) -> None:
        return self.process.start()

    def join_channel(self, channel: str) -> None:
        self.queue.put(channel)
        self.saturation = self.saturation + 1


ALL_SHARDS: List[Shard] = []


def run_bot(queue: Queue) -> None:
    """
    Represents one of the running bot connections.
    We also provide a periodic callback to listen to newly appearing channels.
    """
    # This is a fork. reset all copied signal handlers.
    def noop_signal_handler(sig, frame):
        # ignore signals
        pass

    signal.signal(signal.SIGINT, noop_signal_handler)
    bot = TwitchIrcBot(
        Database.get(True)
    )  # important to recreate the db conn, since it has been forked.

    def between_frames() -> None:
        # this is run when the twitch bot has free time, roughly every 5s.
        try:
            channel = queue.get(timeout=0.1)  # block for no more than 100ms.
            if channel:
                if channel == END_OF_LIFE:
                    # exit command.
                    bot.disconnect()
                    # we need to be careful to empty the queue before exiting, so that
                    # there is not a deadlock.
                    # see: https://stackoverflow.com/questions/31665328/python-3-multiprocessing-queue-deadlock-when-calling-join-before-the-queue-is-em
                    while not queue.empty():
                        queue.get()
                    os._exit(0)
                else:
                    # issue a join command to the twitch bot.
                    bot.do_join(str(channel))
        except Empty:
            # nothing to do.
            pass

    bot.set_periodic(between_frames, 3)
    bot.start()  # note- this blocks + runs indefinitely.


def get_unsaturated_shards() -> List[Shard]:
    """
    Returns all of the subprocesses that can still join more channels.
    If none exist, creates another one.
    """
    unsaturated_shards = list(
        filter(lambda shard: not shard.is_saturated(), ALL_SHARDS)
    )
    if not unsaturated_shards:
        # no free shards available, create one.
        shard = create_shard()
        ALL_SHARDS.append(shard)
        return [shard]
    return unsaturated_shards


def observe_db():
    joined_channels = set()
    """
    A watchdog thread that checks for new channels being added to the DB.
    If new channels are added, this thread one of the twitch bot subprocesses
    to join the channel and listen for messages.

    The db observer thread runs on the MAIN PROCESS. It's
    """
    global SHUTDOWN_INITIATED
    while not SHUTDOWN_INITIATED.isSet():
        time.sleep(4)  # wait a few seconds.
        all_channels = DB.get_channels()
        for i, channel in enumerate(all_channels):
            # TODO: We should use the tracked channels by the IRC bot.
            if channel not in joined_channels:
                target_shards = get_unsaturated_shards()
                target_shard = target_shards[i % len(target_shards)]
                target_shard.join_channel(channel)
                joined_channels.add(channel)
            if (i % int(settings["init_pack_size"])) == 0 and i > 0:
                # take a break!
                SHUTDOWN_INITIATED.wait(int(settings["init_pack_wait_s"]))
            if SHUTDOWN_INITIATED.isSet():
                continue
        if SHUTDOWN_INITIATED.isSet():
            continue
        SHUTDOWN_INITIATED.wait(int(settings["db_observe_frequency"]))
    log.info("Stopped DB observer.")


def signal_handler(sig, frame):
    # Stop the DB Observer.
    global SHUTDOWN_INITIATED
    global DB_OBSERVER_THREAD
    global ABORT_STARTUP
    log.info("Stopping DB observer...")
    SHUTDOWN_INITIATED.set()
    ABORT_STARTUP = True
    if DB_OBSERVER_THREAD:
        DB_OBSERVER_THREAD.join()
    log.info("Stopping shards...")
    for i, shard in enumerate(ALL_SHARDS):
        shard.queue.put(END_OF_LIFE)  # end-of-life signal.
        shard.process.join()
    log.info("Goodbye.")
    os._exit(0)


def create_shard() -> Shard:
    time.sleep(settings["init_shard_wait_s"])
    global TOTAL_SHARDS
    TOTAL_SHARDS = TOTAL_SHARDS + 1
    queue: Queue = Queue()
    process = Process(target=run_bot, args=(queue,))
    process.start()
    return Shard(queue=queue, process=process)


if __name__ == "__main__":
    # Install Ctrl+C handler.
    signal.signal(signal.SIGINT, signal_handler)

    all_channels_count = len(DB.get_channels())
    suggested_shard_size = int(
        settings["shard_size"]
    )  # note- this should be between 50-100 per the twitch documentation.
    proc_count = math.ceil(all_channels_count / suggested_shard_size)
    # pre-create all the shards we'll need for the beginning.
    # note that if the DB grows, we'll only ever grow by one shard at a time.
    log.info("%d channels loaded initially.", all_channels_count)
    log.info("Sharding into %d processes.", proc_count)
    ALL_SHARDS = []
    for _ in range(proc_count):
        ALL_SHARDS.append(create_shard())
        if ABORT_STARTUP:
            break

    # Start observing DB for changes.
    if not ABORT_STARTUP:
        DB_OBSERVER_THREAD = threading.Thread(target=observe_db, args=())
        DB_OBSERVER_THREAD.start()
        log.info("Startup complete.")
    else:
        log.info("Startup aborted.")