#!/usr/bin/python3
import asyncio
import os
import threading
import irc
from irc.bot import SingleServerIRCBot
import time
import requests
from bot.database import db
from bot.config import settings, locale
from bot.base import CommandNotFoundException
from cooldown import check_cooldown, reset_cooldown
from typing import Optional
from bot.base import CommandContext, AuthorInfo
from bot.bot import LogicEFTBot
from bot.log import log
from typing import Any
import signal
import traceback

def check_lang(channel_name: str) -> str:
    return db.get_lang(channel_name)

channels = list(dict.fromkeys(db.get_channels() + settings["initial_channels"]))
IRC_SPEC = (settings["irc_server"], int(settings["irc_port"]), settings["irc_token"])
log.info(f"Connecting to server: {IRC_SPEC}")

class TwitchIrcBot(SingleServerIRCBot):
    def __init__(self):
        super().__init__(
            [IRC_SPEC],
            settings["nick"],
            settings["nick"]
        )
        self.logic = LogicEFTBot()

    def on_welcome(self, connection, event):
        log.info('Received welcome.')
        log.info('Joining (%s) channels.', len(channels))

        # Request specific capabilities before you can use them
        connection.cap('REQ', ':twitch.tv/membership')
        connection.cap('REQ', ':twitch.tv/tags')
        connection.cap('REQ', ':twitch.tv/commands')

        # Rejoin all the channels this bot should be in.
        for i, channel in enumerate(channels):
            self.do_join(channel)
            log.info('Joining `#%s`', channel)
            if (i > 0) and (i % int(settings["init_pack_size"]) == 0):
                # wait a bit before connecting more.
                # twitch rate-limits bots from the amount of JOIN commands
                # they can issue.
                time.sleep(int(settings["init_pack_wait_s"]))

    def do_join(self, channel: str):
        self.connection.join("#" + channel)

    def get_command_context(self, event):
        tags = event.tags
        display_name = None
        is_mod = False
        for tag in tags:
            if tag["key"] == "display-name":
                display_name = tag["value"]
            elif tag["key"] == "mod":
                is_mod = is_mod or tag["value"] == '1'
            elif tag["key"] == "badges":
                is_mod = is_mod or (tag["value"] and "broadcaster/1" in tag["value"])
        channel = event.target[1:] if event.target[0] == "#" else event.target
        return CommandContext(
            author=AuthorInfo(
                name=display_name,
                is_mod=is_mod
            ),
            channel=channel
        )

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
        except Exception as e:
            log.error("Error connecting to the server: %s", str(e))
            pass

    def on_error(self, connection, event):
        log.info("Got error: %s", str(event))

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        c = self.connection
        if msg:
            if msg[:1] == settings["prefix"]:
                parts = event.arguments[0].split()
                cmd = parts[0][1:]
                if not self.logic.has_command(cmd):
                    # ignore commands we don't support.
                    return
                content = ' '.join(parts[1:] or [])
                context = self.get_command_context(event)
                if check_cooldown(db, context.channel):
                    log.info("Cooldown enforced on channel: %s", context.channel)
                    return
                if context.author.name.lower() == settings["nick"]:
                    # ignoring own message.
                    return
                reset_cooldown(context.channel)
                self.do_command(context, event, cmd, content)

    def do_send_msg(self, channel: str, message: str) -> None:
        self.connection.privmsg("#" + channel, message)

    def do_command(self, context: CommandContext, event: Any, command: str, content: Optional[str]):
        c = self.connection
        try:
            resp = self.logic.exec(context, command, content)
            if resp:
                self.do_send_msg(context.channel, resp)
        except CommandNotFoundException:
            # just be silent if we don't know the command.
            pass
        except Exception as e:
            # Log all other exceptions.
            log.error(f"Exception processing command ({command}) for channel ({context.channel}) -")
            log.error(e)
            traceback.print_exc()

def observe_db():
    """
    A watchdog thread that checks for new channels being added to the DB.
    If new channels are added, this thread asks the twitch bot to join
    the channel and listen for messages.
    """
    while DB_OBSERVER_THREAD_LIVE:
        time.sleep(4) # wait a few seconds.
        log.info("[observe_db] Scanning for new channels in DB.\n")
        # load all channels from db.
        all_channels = db.get_channels()
        for channel in all_channels:
            if channel not in channels:
                # join the channel + add to tracked channels.
                # TODO: We should use the tracked channels by the IRC bot,
                # and not the 'channels' list.
                TWITCH_BOT.do_join(channel)
                channels.append(channel)
        # wait until next time.
        time.sleep(int(settings["db_observe_frequency"]))
    log.info("Stopped DB observer.")

DB_OBSERVER_THREAD = None
DB_OBSERVER_THREAD_LIVE = True
TWITCH_BOT = None

def signal_handler(sig, frame):
    log.info("Received request to kill bot.")
    os._exit(0)

# Install Ctrl+C handler.
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    # Start observing DB for changes.
    DB_OBSERVER_THREAD = threading.Thread(target=observe_db, args=())
    DB_OBSERVER_THREAD.start()

    # Start bot.
    TWITCH_BOT = TwitchIrcBot()
    log.info("Starting bot. (Ctrl + C to exit)")
    TWITCH_BOT.start()
