#!/usr/bin/python3

import discord
import os
from cooldown import check_cooldown, reset_cooldown
from bot.config import settings, localized_string
from bot.eft import EFT
from bot.bot import LogicEFTBot
from bot.base import CommandContext, AuthorInfo, CommandNotFoundException, command
from bot.log import log
from bot.database import Database
from discord import Client
import signal
import traceback
from typing import Union


class DiscordEFTBot(LogicEFTBot):
    """
    Any commands that you want to override to have special behavior for discord,
    you can override in this class.
    """

    @command("price", "p")
    def bot_price(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        info = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "price",
            info.name,
            info.price,
            info.updated.strftime("%m/%d/%Y %H:%M"),
        )
        embed = discord.Embed(
            title="LogicEFTBot",
            url="https://eft.bot",
            description="The Free Tarkov Bot",
            color=0x780A81,
        )
        embed.set_thumbnail(url=info.img)
        embed.add_field(name=info.name, value=response, inline=True)
        return embed


class DiscordClient(Client):
    """
    A discord client for LogicEFTBot.
    To run: `export LOGIC_DISCORD_TOKEN=<token> && make discord`
    Where <token> is the valid oauth token for executing this bot.
    """

    def __init__(self):
        super().__init__()
        self.logic = DiscordEFTBot(Database.get())

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Game(name="!eftbot - https://eft.bot")
        )
        print("Connected and Discord Status Set")

    async def on_message(self, message):
        full_cmd = message.content.split()
        if not full_cmd:
            return
        cmd = full_cmd[0]
        if not cmd:
            return
        if not cmd[0] == settings["prefix"]:
            return
        cmd = cmd[len(settings["prefix"]) :]  # skip past "!"

        # check cooldown for this channel.
        guild = message.guild
        if not guild:
            return
        channel = str(
            guild.id
        )  # this is a unique int representing this discord server.
        author = message.author
        is_mod = (
            author.guild_permissions.administrator
            if author.guild_permissions
            else False
        )
        context = CommandContext(
            author=AuthorInfo(name=message.author.display_name, is_mod=is_mod),
            channel=channel,
            platform="discord",
        )
        db = Database.get()
        content = " ".join(full_cmd[1:] or [])
        if check_cooldown(db, context.channel):
            # Enforce cooldown for this channel.
            return
        try:
            resp = self.logic.exec(context, cmd, content)
            if isinstance(resp, str):
                await message.channel.send(resp)
            elif isinstance(resp, discord.Embed):
                await message.channel.send(embed=resp)
            else:
                log.error("Unknown response: {}".format(str(resp)))
            reset_cooldown(context.channel)
        except CommandNotFoundException:
            # just be silent if we don't know the command.
            pass
        except Exception as e:
            # Log all other exceptions.
            log.error(
                f"Exception processing command ({cmd}) for channel '{guild.name}' (id={context.channel}) -"
            )
            log.error(e)
            traceback.print_exc()


def signal_handler(sig, frame):
    log.info("Received request to kill bot.")
    os._exit(0)


# Install Ctrl+C handler.
signal.signal(signal.SIGINT, signal_handler)


def main():
    token = os.environ.get("LOGIC_DISCORD_TOKEN")
    if not token:
        print(
            "Error: Please set `export LOGIC_DISCORD_TOKEN=<token>` and re-run the bot.\n"
        )
        return
    client = DiscordClient()
    client.run(token)


if __name__ == "__main__":
    main()
