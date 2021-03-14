
from irc.bot import SingleServerIRCBot
from queue import Empty
from typing import Optional, Callable
from multiprocessing import Queue, Process
import json
from dataclasses import dataclass
from bot.config import settings
import sys
import os

TOKEN = os.environ.get("CHATMEMBER_TOKEN")
NICK = "irctestbot"

IRC_SPEC = (settings["irc_server"], int(settings["irc_port"]), TOKEN)

@dataclass
class ChatMemberCommand:
    exit: Optional[bool] = False
    join: Optional[str] = None
    say: Optional[str] = None

@dataclass
class ChatMemberResponse:
    welcome: bool = False
    shutdown: bool = False
    message: Optional[str] = None
    connected: bool = False

class ChatMember(SingleServerIRCBot):
    def __init__(self, inbound: Queue, outbound: Queue):
        super().__init__([IRC_SPEC], NICK, NICK)
        self.inbound = inbound
        self.outbound = outbound
        self.is_welcome = False
        self.channel = None
        self.set_periodic(self.on_tick, .3)

    def on_tick(self):
        # poll inbound queue for messages
        try:
            command = self.inbound.get(block=False)
            if command:
                if command.say:
                    self.do_send_msg(self.channel, command.say)
                elif command.join:
                    self.do_join(command.join)
                elif command.exit:
                    self.disconnect()
                    self.outbound.put(ChatMemberResponse(shutdown=True))
                    sys.exit() # if sys.exit is called from wtihin a thread, it only ends that thread.
                    return
        except Empty:
            pass

    def on_error(self, connection, event):
        print(f"Got error: {str(event)}")

    def on_welcome(self, connection, event):
        # Request specific capabilities before you can use them
        connection.cap("REQ", ":twitch.tv/membership")
        # Tell the test we got our welcome call
        self.outbound.put(ChatMemberResponse(welcome=True))

    def _connect(self):
        """
        Establish a connection to the server at the front of the server_list.
        """
        server = self.servers.peek()
        try:
            self.connect(
                server.host,
                server.port,
                self._nickname,
                server.password,
                ircname=self._realname,
            )
            self.outbound.put(ChatMemberResponse(connected=True))
        except Exception as e:
            log.error("Error connecting to the server: %s", str(e))
            self.outbound.put(ChatMemberResponse(shutdown=True, message="Error connecting to server."))
            sys.exit() # if sys.exit is called from wtihin a thread, it only ends that thread.

    def do_join(self, channel: str) -> None:
        self.connection.join("#" + channel)
        self.channel = channel

    def _on_disconnect(self, connection, event):
        super()._on_disconnect(connection, event)
        # This is overridden to avoid reconnect strategy.

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        if msg:
            self.outbound.put(ChatMemberResponse(message=msg))

    def do_send_msg(self, channel: str, message: str) -> None:
        self.connection.privmsg("#" + channel, message)

    def set_periodic(self, fn: Callable, frequency_s: int):
        """
        Set a function to run every <n> seconds.
        """
        self.reactor.scheduler.execute_every(frequency_s, fn)

if __name__ == "__main__":
    chatMember = ChatMember(Queue(), Queue(), "pawn_star")
    chatMember.start()
