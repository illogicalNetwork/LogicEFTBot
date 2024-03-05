from twitchio.ext import commands

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


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
            token="oauth:iqtmm142vvtovkv41frm5zpgnecwif",
            prefix="!!",
            initial_channels=["#logicalsolutions"],
        )

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


bot = Bot()
bot.run()
