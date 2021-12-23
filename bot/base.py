from multiprocessing import Queue
from typing import Optional, Any, Callable, Dict, List
from inspect import signature, iscoroutinefunction
from dataclasses import dataclass
from bot.log import log
from bot.database import Database

"""
This is the python implementation of the commands
of LogicEFT bot.

This should be shared with any of the front-ends which use the bot
(e.g twitch, discord).
"""


class CommandNotFoundException(Exception):
    def __init__(self, command: str) -> None:
        super().__init__(f"Command ${command} not found.")


def command(*names: str):
    """
    Decorator to support marking a function as a command.
    """

    def decorator(func: Any):
        sig = signature(func)
        # TODO: We should also technically validate the parameter types here too.
        # i.e the (context, cmd, data) structure.
        if not sig.return_annotation or iscoroutinefunction(func):
            # def doesn't have correct signature
            raise Exception(
                f"Function {func.__name__} cannot be attached to command `{','.join(names)}`. It must have the signature: (..) -> Any."
            )
        func._bot_command = names  # type: ignore
        return func

    decorator._bot_command = names  # type: ignore
    return decorator


@dataclass(frozen=True)
class AuthorInfo:
    name: str
    """
    Whether the author is a moderator of the channel the bot is in.
    """
    is_mod: bool
    """
    Whether the author is an admin (i.e LogicalSolutions)
    """
    is_admin: bool


@dataclass(frozen=True)
class CommandContext:
    author: AuthorInfo
    channel: str
    platform: str  # Literal["twitch", "discord"]


CommandType = Callable[[CommandContext, Optional[str]], str]
CommandCacheType = Dict[str, CommandType]


class LogicEFTBotBase:
    """
    A base class for implementing the EFT bot.
    Provides the logic for automatically registering commands.
    """

    def has_command(self, cmd: str):
        return cmd in self.commands

    def __init__(self, db: Database, inputQueue: Queue, outputQueue: Queue):
        # read all methods on this object and cache them.
        self.db = db
        self.commands: CommandCacheType = {}
        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

        for attr in dir(self):
            obj = getattr(self, attr)
            if attr.startswith("__") or not callable(obj):
                # this is not a fn
                continue
            if not hasattr(obj, "_bot_command"):
                # doesn't have a command fn annotation
                continue
            names = getattr(obj, "_bot_command")
            for name in names:
                name = name.lower()
                if name in self.commands:
                    # command already exists.
                    raise Exception(
                        f"LogicEFTBot has duplicate commands registered for ${name}"
                    )
                self.commands[name] = obj

    def exec(self, ctx: CommandContext, command: str, data: Optional[str]) -> str:
        """
        Execute a bot command given by `!command <data>`, where data is some
        optional string included after the command.
        """
        # attempt to resolve the alias
        aliases = self.db.get_command_aliases(ctx.channel)
        if aliases:
            command = command.lower()  # cmds are case-insensitive
            if command in aliases:
                command = aliases[command]  # resolve the alias
        # search for command
        if not command in self.commands:
            raise CommandNotFoundException(command)
        fn = self.commands[command]
        #if data is not "":
         #   self.db.sql_log(ctx.platform, ctx.channel, command, data)
        return fn(ctx, data)
