from typing import Callable, List, Any
import signal
import threading
import math
from typing import List
from dataclasses import dataclass
from multiprocessing import Queue, Process
from twitch import TwitchIrcBot
from bot.database import Database
from bot.config import settings
from bot.log import log

DB : Database = Database.get()
DB_OBSERVER_THREAD = None
DB_OBSERVER_THREAD_LIVE = True
END_OF_LIFE = -1

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
        return self.saturation < int(settings['shard_size'])

    def start(self) -> None:
        return self.process.start()

    def join_channel(self, channel: str) -> None:
        self.queue.put(channel)
        self.saturation = self.saturation + 1


def run_bot(queue: Queue) -> None:
    """
    Represents one of the running bot connections.
    We also provide a periodic callback to listen to newly appearing channels.
    """
    bot = TwitchIrcBot(DB)
    def between_frames() -> None:
        # this is run when the twitch bot has free time, roughly every 5s.
        channel = queue.get(timeout=.1) # block for no more than 100ms.
        if channel:
            if channel == END_OF_LIFE:
                # exit command.
                bot.disconnect()
                # we need to be careful to empty the queue before exiting, so that
                # there is not a deadlock.
                # see: https://stackoverflow.com/questions/31665328/python-3-multiprocessing-queue-deadlock-when-calling-join-before-the-queue-is-em
                while not queue.empty():
                    queue.get()
            else:
                # issue a join command to the twitch bot.
                bot.do_join(str(channel))
    bot.set_periodic(between_frames, 3)
    bot.start() # note- this blocks + runs indefinitely.

ALL_SHARDS : List[Shard] = []

def get_unsaturated_shards() -> List[Shard]:
    """
    Returns all of the subprocesses that can still join more channels.
    If none exist, creates another one.
    """
    unsaturated_shards = list(filter(lambda shard: not shard.is_saturated(), ALL_SHARDS))
    if not unsaturated_shards:
        # no free shards available, create one.
        shard = create_shard()
        ALL_SHARDS.append(shard)
        shard.start()
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
    while DB_OBSERVER_THREAD_LIVE:
        time.sleep(4) # wait a few seconds.
        all_channels = db.get_channels()
        for i, channel in enumerate(all_channels):
            # TODO: We should use the tracked channels by the IRC bot.
            if channel not in joined_channels:
                target_shards = get_unsaturated_shards()
                target_shard = target_shards[i % len(target_shards)]
                target_shard.join_channel(channel)
                joined_channels.append(channel)
        time.sleep(int(settings["db_observe_frequency"]))
    log.info("Stopped DB observer.")

def signal_handler(sig, frame):
    # Stop the DB Observer.
    DB_OBSERVER_THREAD_LIVE = False
    DB_OBSERVER_THREAD.join()
    for i, queue in enumerate(COMM_QUEUES):
        queue.put(END_OF_LIFE) # end-of-life signal.
        ALL_PROCESSES[i].join()
    log.info("Received request to kill bot.")
    os._exit(0)

# Install Ctrl+C handler.
signal.signal(signal.SIGINT, signal_handler)

def create_shard() -> Shard:
    queue: Queue = Queue()
    process = Process(target=run_bot, args=(queue, ))
    return Shard(queue=queue, process=process)

if __name__ == "__main__":
    all_channels_count = len(DB.get_channels())
    suggested_shard_size = int(settings["shard_size"]) # note- this should be between 50-100 per the twitch documentation.
    proc_count = math.ceil(all_channels_count / suggested_shard_size)
    # pre-create all the shards we'll need for the beginning.
    # note that if the DB grows, we'll only ever grow by one shard at a time.
    log.info("Sharding into %d processes.", proc_count)
    ALL_SHARDS = [create_shard() for _ in range(proc_count)]
    for shard in ALL_SHARDS:
        shard.start()
        log.info("Started shard with pid %d", shard.process.pid)

    # Start observing DB for changes.
    log.info("Listening for DB changes.")
    DB_OBSERVER_THREAD = threading.Thread(target=observe_db, args=())
    DB_OBSERVER_THREAD.start()

    log.info("Startup complete.")
