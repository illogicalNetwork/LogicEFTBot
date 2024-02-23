#!/usr/bin/python3
from irc.bot import SingleServerIRCBot
from multiprocessing import Queue
from logiceftbot.common.database import Database
from logiceftbot.common.config import settings
from logiceftbot.common.base import CommandNotFoundException
from logiceftbot.twitch.cooldown import check_cooldown, reset_cooldown
from typing import Optional
from logiceftbot.common.base import CommandContext, AuthorInfo
from logiceftbot.common.bot import LogicEFTBot
from logiceftbot.common.log import log
from typing import Any, Callable, List, Set
import traceback

IRC_SPEC = (settings["irc_server"], int(settings["irc_port"]), settings["irc_token"])


class TwitchIrcBot(SingleServerIRCBot):
    """_summary_

    Args:
        SingleServerIRCBot (_type_): _description_

    Returns:
        _type_: _description_
    """

    APPROVED_ADMINS = ["LogicalSolutions"]

    def __init__(self, db: Database, inputQueue: Queue, outputQueue: Queue):
        super().__init__([IRC_SPEC], settings["nick"], settings["nick"])
        self.db = db
        self.logic = LogicEFTBot(db, inputQueue, outputQueue)
        self.status = "Startup"
        self.message = "Initializing"
        self.enqueued_channels: List[str] = []
        self.joined_channels: Set[str] = set()
        self.is_welcome = False
        self.processed_commands = 0

    def on_welcome(self, connection, event):
        """_summary_

        Args:
            connection (_type_): _description_
            event (_type_): _description_
        """
        connection.cap("REQ", ":twitch.tv/membership")
        connection.cap("REQ", ":twitch.tv/tags")
        connection.cap("REQ", ":twitch.tv/commands")
        self.is_welcome = True
        self.message = "Running"

        if self.enqueued_channels:
            log.info("Joining %d channels", len(self.enqueued_channels))
            for chan in self.enqueued_channels:
                self.do_join(chan)
        self.enqueued_channels.clear()

    def do_broadcast(self, message: str) -> None:
        """_summary_

        Args:
            message (str): _description_
        """
        log.info("Broadcast: %s", message)
        recently_active_channels = self.db.get_recently_active_channels()
        for channel in self.joined_channels:
            if channel in recently_active_channels:
                self.do_send_msg(channel, message)

    def do_join(self, channel: str) -> None:
        """_summary_

        Args:
            channel (str): _description_
        """
        if channel in self.joined_channels:
            return
        if not self.connection.connected:
            if self.is_welcome:
                log.info(
                    "ERROR: We've been rate limited. ------------------------------------"
                )
                return
            self.enqueued_channels.append(channel)
        else:
            log.info("Joining '#%s'", channel)

            self.status = ":rocket: Joining"
            self.message = f"#{channel}"
            self.connection.join("#" + channel)
            self.joined_channels.add(channel)
            self.status = ":white_heavy_check_mark: Healthy"
            self.message = "Connected"

    def get_command_context(self, event):
        """_summary_

        Args:
            event (_type_): _description_

        Returns:
            _type_: _description_
        """
        tags = event.tags
        display_name = None
        is_mod = False
        for tag in tags:
            if tag["key"] == "display-name":
                display_name = tag["value"]
            elif tag["key"] == "mod":
                is_mod = is_mod or tag["value"] == "1"
            elif tag["key"] == "badges":
                is_mod = is_mod or (tag["value"] and "broadcaster/1" in tag["value"])
        channel = event.target[1:] if event.target[0] == "#" else event.target
        is_admin = (
            display_name is not None
        ) and display_name in TwitchIrcBot.APPROVED_ADMINS
        return CommandContext(
            author=AuthorInfo(name=display_name, is_mod=is_mod, is_admin=is_admin),
            channel=channel,
            platform="twitch",
        )

    def _connect(self):
        """
        Establish a connection to the server at the front of the server_list.
        """
        server = self.servers.peek()
        self.status = ":mobile_phone_with_arrow: Connecting"
        self.message = "Reaching twitch..."
        try:
            self.connect(
                server.host,
                server.port,
                self._nickname,
                server.password,
                ircname=self._realname,
            )
            self.status = ":white_heavy_check_mark: Healthy"
            self.message = "Connected"
        except Exception as e:
            log.error("Error connecting to the server: %s", str(e))
            pass

    def on_error(self, connection, event):
        log.info("Got error: %s", str(event))
        self.status = "Exception"
        self.message = str(event)

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        if msg:
            if msg[:1] == settings["prefix"]:
                parts = event.arguments[0].lower()
                if "gpu" in parts:
                    parts = parts.replace("gpu", "graphics card")
                parts = parts.split()
                cmd = parts[0][1:]
                content = " ".join(parts[1:] or [])
                context = self.get_command_context(event)
                if check_cooldown(self.db, context.channel):
                    # Cooldown enforced on channel
                    return
                if context.author.name.lower() == settings["nick"]:
                    # ignoring own message.
                    return
                self.processed_commands = self.processed_commands + 1
                self.do_command(context, event, cmd, content)

    def do_send_msg(self, channel: str, message: str) -> None:
        self.connection.privmsg("#" + channel, message)

    def do_command(
        self, context: CommandContext, event: Any, command: str, content: Optional[str]
    ):
        try:
            resp = self.logic.exec(context, command, content)
            if resp:
                self.do_send_msg(context.channel, f"{context.author.name}: {resp}")
                reset_cooldown(context.channel)
        except CommandNotFoundException:
            # just be silent if we don't know the command.
            pass
        except Exception as e:
            # Log all other exceptions.
            log.error(
                f"Exception processing command ({command}) for channel ({context.channel}) -"
            )
            log.error(str(e))
            traceback.print_exc()

    def set_periodic(self, fn: Callable, frequency_s: int):
        """
        Set a function to run every <n> seconds.
        """
        self.reactor.scheduler.execute_every(frequency_s, fn)
