#!/usr/bin/python3

import discord
import os
from cooldown import check_cooldown, reset_cooldown
from bot.config import settings, localized_string
from bot.eft import EFT
from bot.bot import LogicEFTBot
from bot.base import CommandContext, AuthorInfo, CommandNotFoundException, command
from bot.log import log
from bot.models import (
    safe_int,
)
from bot.database import Database
from discord import Client
import signal
import traceback
import maya
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
        try:
            price = EFT.check_price(lang, data)
            embed = discord.Embed(
                title=price.name,
                url=price.wikiLink,
                color=0x780A81,
            )
            embed.set_thumbnail(url=price.img)
            embed.add_field(
                name=localized_string(lang, "marketPrice"),
                value=format(int(price.price), ","),
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "marketTrader"),
                value=price.traderName,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "marketTraderPrice"),
                value=format(int(price.traderPrice), ","),
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "marketSlot"),
                value=format(round((price.price / price.slots)), ","),
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "market7dAvg"),
                value=format(int(price.avg7daysPrice), ","),
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "market24hAvg"),
                value=format(int(price.avg24hPrice), ","),
                inline=True,
            )
            embed.set_footer(
                text=localized_string(lang, "marketUpdated")
                + maya.MayaDT.from_datetime(price.updated).slang_time()
            )
            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid item ; please try again.",
                inline=True,
            )
            return embed

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            astat = EFT.check_astat(lang, data)
            embed = discord.Embed(
                title=astat.name,
                url=astat.wikiLink,
                description=astat.description,
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://static.tarkov-database.com/image/icon/1-1/{0}.png".format(
                    astat.bsgID
                )
            )
            embed.add_field(
                name=localized_string(lang, "ammoFlesh"),
                value=astat.damage,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "ammoPen"),
                value=astat.penetration,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "ammoArmor"),
                value=astat.armorDamage,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "ammoAccuracy"),
                value=astat.accuracy,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "ammoRecoil"),
                value=astat.recoil,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "ammoFrag"),
                value=astat.fragmentation,
                inline=True,
            )
            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid ammo item ; please try again.",
                inline=True,
            )
            return embed

    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            armor = EFT.check_armor(lang, data)
            embed = discord.Embed(
                title=armor.armorName,
                url=armor.wikiLink,
                description=localized_string(lang, "armorZones") + armor.armorZones,
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://static.tarkov-database.com/image/icon/1-1/{0}.png".format(
                    armor.bsgID
                )
            )
            embed.add_field(
                name=localized_string(lang, "armorClass"),
                value=armor.armorClass,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "armorMaterial"),
                value=armor.armorMaterial,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "armorDurability"),
                value=armor.armorDurability,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "armorMoveSpeed"),
                value=armor.armorMoveSpeed,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "armorTurnSpeed"),
                value=armor.armorTurnSpeed,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "armorErgo"),
                value=armor.armorErgo,
                inline=True,
            )
            embed.set_footer(
                text=localized_string(lang, "armorEffectiveDurability")
                + armor.armorEffectiveDurability
            )
            return embed
        except Exception as e:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid armor item ; please try again.",
                inline=True,
            )
            print(e)
            return embed

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            helmet = EFT.check_helmets(lang, data)
            embed = discord.Embed(
                title=helmet.name,
                url=helmet.wikiLink,
                description=helmet.description,
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://static.tarkov-database.com/image/icon/1-1/{0}.png".format(
                    helmet.bsgID
                )
            )
            embed.add_field(
                name=localized_string(lang, "helmetZones"),
                value=helmet.armorZones,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetClass"),
                value=helmet.armorClass,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetDurability"),
                value=helmet.armorDurability,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetRicochet"),
                value=helmet.armorRico,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetMoveSpeed"),
                value=helmet.armorMoveSpeed,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetTurnSpeed"),
                value=helmet.armorTurnSpeed,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetErgo"),
                value=helmet.armorErgo,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetSoundReduc"),
                value=helmet.helmetSoundReduc,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "helmetBlocksHeadset"),
                value=helmet.helmetBlocksHeadset,
                inline=True,
            )
            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid helmet item ; please try again.",
                inline=True,
            )
            return embed

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            medical = EFT.check_medical(lang, data)
            embed = discord.Embed(
                title=medical.name,
                url=medical.wikiLink,
                description=medical.description,
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://static.tarkov-database.com/image/icon/1-1/{0}.png".format(
                    medical.bsgID
                )
            )
            embed.add_field(
                name=localized_string(lang, "medUseTime"),
                value=medical.useTime,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "maxItemHP"),
                value=medical.resources,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "maxHealPerUse"),
                value=medical.resourceRate,
                inline=True,
            )

            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid medical item ; please try again.",
                inline=True,
            )
            return embed

    @command("maps")
    def bot_maps(self, ctx: CommandContext, data: str) -> Union[str, discord.Embed]:
        log.info("%s - searching for %s (new)\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            maps = EFT.check_maps(lang, data)
            embed = discord.Embed(
                title=maps.name,
                url=maps.wikiLink,
                description=maps.features,
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://eft.bot/images/wiki/{0}.png".format(maps.shortName)
            )
            embed.add_field(
                name=localized_string(lang, "mapPlayers"),
                value=maps.players,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "mapDuration"),
                value=maps.duration,
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "mapEnemies"),
                value=maps.enemies,
                inline=True,
            )
            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid map name ; please try again.",
                inline=True,
            )
            return embed

    @command("tax")
    def calculate_tax(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            USAGE = localized_string(lang, "taxUsage")
            if not data:
                return USAGE
            parts = data.split()
            if len(parts) < 2:
                return localized_string(lang, "taxUsage")
            amount = safe_int(parts[0], 0)
            if amount == 0:
                return USAGE
            query = " ".join(parts[1:])
            tax_amount = EFT.check_tax(lang, amount, query)
            if not tax_amount:
                return USAGE
            (tax, model) = tax_amount
            profit = amount - tax
            embed = discord.Embed(
                title=model.name,
                url=model.wikiLink,
                color=0x780A81,
            )
            embed.set_thumbnail(url=model.img)
            embed.add_field(
                name=localized_string(lang, "taxBasePrice"),
                value=format(int(model.basePrice), ",") + " ₽",
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "taxBaseTax"),
                value=format(int(tax), ",") + " ₽",
                inline=True,
            )
            embed.add_field(
                name=localized_string(lang, "taxProfit"),
                value=format(int(profit), ",") + " ₽",
                inline=True,
            )
            embed.set_footer(
                text=localized_string(lang, "marketUpdated")
                + maya.MayaDT.from_datetime(model.updated).slang_time()
            )
            return embed
        except:
            embed = discord.Embed(
                title="LogicEFTBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            embed.add_field(
                name="Invalid Item Search",
                value="You've entered in an invalid map name ; please try again.",
                inline=True,
            )
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
