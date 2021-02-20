
from irc.bot import SingleServerIRCBot
from queue import Empty
from multiprocessing import Queue, Process
import json

class ChatMember(SingleServerIRCBot):
    def __init__(self, inbound: Queue, outbound: Queue):
        super().__init__([IRC_SPEC], settings["nick"], settings["nick"])
        self.db = db
        self.logic = LogicEFTBot(db)
        self.enqueued_channels: List[str] = []
        self.joined_channels: Set[str] = set()
        self.is_welcome = False
        self.set_periodic(self.on_tick, 0.5)

    def on_tick(self):
        pass

    def on_welcome(self, connection, event):
        # Request specific capabilities before you can use them
        connection.cap("REQ", ":twitch.tv/membership")
        connection.cap("REQ", ":twitch.tv/tags")
        connection.cap("REQ", ":twitch.tv/commands")
        self.is_welcome = True  # we've received welcome.

        if self.enqueued_channels:
            log.info("Joining %d channels", len(self.enqueued_channels))
            for chan in self.enqueued_channels:
                self.do_join(chan)
        self.enqueued_channels = []

    def do_join(self, channel: str) -> None:
        log.info("Joining '#%s'", channel)
        self.connection.join("#" + channel)

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        c = self.connection
        if msg:
            outbound.put(msg)

    def do_send_msg(self, channel: str, message: str) -> None:
        self.connection.privmsg("#" + channel, message)

    def set_periodic(self, fn: Callable, frequency_s: int):
        """
        Set a function to run every <n> seconds.
        """
        self.reactor.scheduler.execute_every(frequency_s, fn)
