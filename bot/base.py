from typing import Optional, Any, Callable, Dict
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


def command(name: str):
    """
    Decorator to support marking a function as a command.
    """

    def decorator(func: Any):
        sig = signature(func)
        # TODO: We should also technically validate the parameter types here too.
        # i.e the (context, cmd, data) structure.
        if sig.return_annotation is not str or iscoroutinefunction(func):
            # def doesn't have correct signature
            raise Exception(
                f"Function {func.__name__} cannot be attached to command `{name}`. It must have the signature: (..) -> str."
            )
        func._bot_command = name  # type: ignore
        return func

    decorator._bot_command = name  # type: ignore
    return decorator


@dataclass(frozen=True)
class AuthorInfo:
    name: str
    is_mod: str


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

    def __init__(self, db: Database):
        # read all methods on this object and cache them.
        self.db = db
        self.commands: CommandCacheType = {}
        for attr in dir(self):
            obj = getattr(self, attr)
            if attr.startswith("__") or not callable(obj):
                # this is not a fn
                continue
            if not hasattr(obj, "_bot_command"):
                # doesn't have a command fn annotation
                continue
            cmd = getattr(obj, "_bot_command").lower()
            if cmd in self.commands:
                # command already exists.
                raise Exception(
                    f"LogicEFTBot has duplicate commands registered for ${cmd}"
                )
            self.commands[cmd] = obj

    def exec(self, ctx: CommandContext, command: str, data: Optional[str]) -> str:
        """
        Execute a bot command given by `!command <data>`, where data is some
        optional string included after the command.
        """
        # search for command
        if not command in self.commands:
            raise CommandNotFoundException(command)
        fn = self.commands[command]
        if data is not '':
            self.db.sql_log(ctx.platform, ctx.channel, command, data)
        return fn(ctx, data)