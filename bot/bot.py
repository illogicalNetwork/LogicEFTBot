from typing import Optional, Any, Callable
import requests
from inspect import signature
from bot.base import LogicEFTBotBase, command, CommandContext, AuthorInfo
from bot.eft import EFT
from bot.models import (
    safe_int,
)
from bot.database import Database
from bot.log import log
from bot.config import settings, localized_string
from bot.shardupdate import ShardUpdate
import maya


class LogicEFTBot(LogicEFTBotBase):
    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            armor = EFT.check_armor(lang, data)
            return localized_string(
                lang,
                "twitch_armor",
                armor.armorName,
                armor.armorClass,
                armor.armorDurability,
                armor.armorZones,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("armorstats")
    def bot_armorstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            armor = EFT.check_armor(lang, data)
            return localized_string(
                lang,
                "twitch_armorstats",
                armor.armorName,
                armor.armorEffectiveDurability,
                armor.armorMoveSpeed,
                armor.armorTurnSpeed,
                armor.armorErgo,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            astat = EFT.check_astat(lang, data)
            return localized_string(
                lang,
                "twitch_astat",
                astat.name,
                astat.damage,
                astat.penetration,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("avg7d")
    def bot_avg7d(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            avg7d = EFT.check_price(lang, data)
            return localized_string(
                lang,
                "twitch_avg7d",
                avg7d.name,
                format(int(avg7d.avg7daysPrice), ","),
                maya.MayaDT.from_datetime(avg7d.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("avg24h")
    def bot_avg24h(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            avg24h = EFT.check_price(lang, data)
            return localized_string(
                lang,
                "twitch_avg24h",
                avg24h.name,
                format(int(avg24h.avg24hPrice), ","),
                maya.MayaDT.from_datetime(avg24h.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            helmet = EFT.check_helmets(lang, data)
            return localized_string(
                lang,
                "twitch_helmet",
                helmet.name,
                helmet.armorClass,
                helmet.armorDurability,
                helmet.armorRico,
                helmet.armorZones,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("helmetstats")
    def bot_helmetstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            helmet = EFT.check_helmets(lang, data)
            return localized_string(
                lang,
                "twitch_helmetstats",
                helmet.name,
                helmet.armorMoveSpeed,
                helmet.armorTurnSpeed,
                helmet.armorErgo,
                helmet.helmetSoundReduc,
                helmet.helmetBlocksHeadset,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("kappaitem")
    def bot_kappaitem(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            kappa = EFT.check_kappaitem(lang, data)
            return localized_string(
                lang,
                "twitch_kappaItems",
                kappa.quantity,
                kappa.name,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "twitch_notKappaItem",
            )

    @command("kappaquest")
    def bot_kappaquest(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            kappa = EFT.check_kappaquests(lang, data)
            return localized_string(
                lang,
                "twitch_kappaQuests",
                kappa.isReq,
                kappa.name,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("maps")
    def bot_maps(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            maps = EFT.check_maps(lang, data)
            return localized_string(
                lang,
                "twitch_maps",
                maps.name,
                maps.players,
                maps.duration,
                maps.enemies,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            medical = EFT.check_medical(lang, data)
            return localized_string(
                lang,
                "twitch_medical",
                medical.name,
                medical.useTime,
                medical.resources,
                medical.resourceRate,
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("profit")
    def bot_profit(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            return localized_string(
                lang,
                "twitch_profit",
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("price", "p")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            price = EFT.check_price(lang, data)
            return localized_string(
                lang,
                "twitch_price",
                price.name,
                format(int(price.price), ","),
                maya.MayaDT.from_datetime(price.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

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
            if len(parts[0]) > 9:
                return "The item amount cannot exceed 9 digits."
            amount = safe_int(parts[0], 0)
            if amount == 0:
                return USAGE
            query = " ".join(parts[1:])
            tax_amount = EFT.check_tax(lang, amount, query)
            if not tax_amount:
                return USAGE
            (tax, model) = tax_amount
            profit = amount - tax
            return localized_string(
                lang,
                "twitch_tax",
                model.name,
                format(int(amount), ","),
                format(int(tax), ","),
                format(int(profit), ","),
                maya.MayaDT.from_datetime(model.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("trader")
    def bot_trader(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            trader = EFT.check_price(lang, data)
            return localized_string(
                lang,
                "twitch_trader",
                trader.name,
                trader.traderName,
                format(int(trader.traderPrice), ","),
                maya.MayaDT.from_datetime(trader.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            slot = EFT.check_price(lang, data)
            return localized_string(
                lang,
                "twitch_slot",
                slot.name,
                format(int((slot.price / slot.slots)), ","),
                maya.MayaDT.from_datetime(slot.updated).slang_time(),
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("status")
    def bot_status(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            status = EFT.tarkovStatus(lang, data)
            return localized_string(
                lang,
                "tarkovStatus",
                status.name,
                status.status
            )
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            wiki = EFT.check_price(lang, data)
            return localized_string(lang, "twitch_wiki", wiki.name, wiki.wikiLink)
        except Exception as e:
            print("There was a search type error in a channel")
            return localized_string(
                lang,
                "searchFailed",
            )

    ###################### GENERAL INFO COMMANDS ######################################
    @command("eftbot")
    def eft_bot(self, ctx: CommandContext, _=None) -> str:
        return localized_string(self.db.get_lang(ctx.channel), "botHelp")

    @command("help")
    def bot_help(self, ctx: CommandContext, _=None) -> str:
        return localized_string(self.db.get_lang(ctx.channel), "botHelp")

    @command("news", "changes")
    def bot_changes(self, ctx: CommandContext, _=None) -> str:
        return localized_string(self.db.get_lang(ctx.channel), "botChanges")

    @command("addbot")
    def bot_add_bot(
        self, ctx: CommandContext, _=None
    ) -> str:  # Later change this to invite link
        return localized_string(self.db.get_lang(ctx.channel), "addBot")

    ######################## MOD COMMANDS ############################################
    @command("setCD")
    def bot_set_cd(
        self, ctx: CommandContext, cooldown_time=settings["default_cooldown"]
    ) -> str:
        if not ctx.author.is_mod:
            # TODO: unlocalized string.
            return "You ain't a mod you dingus!"
        self.db.update_cooldown(ctx.channel, cooldown_time)
        return "Cooldown has been set to {}".format(cooldown_time)

    @command("setLang")
    def bot_set_lang(
        self, ctx: CommandContext, lang: str = settings["default_lang"]
    ) -> str:
        if not ctx.author.is_mod:
            return "You ain't a mod you dingus!"
        self.db.update_lang(ctx.channel, lang, ctx.channel)
        return "@" + ctx.author.name + " - Language has been set to {}".format(lang)

    @command("alias")
    def bot_alias(self, ctx: CommandContext, data: str) -> str:
        if not ctx.author.is_mod:
            return "You ain't a mod you dingus!"
        parts = data.split() if data else None
        if not parts or len(parts) != 2:
            return "Usage: !alias <alias> <existingCommand>"
        alias = parts[0].lower()
        existingCommand = parts[1].lower()
        if alias in self.commands:
            return f"Alias `{alias}` would overwrite an existing command. Please choose another alias."
        if not existingCommand in self.commands:
            return "Can't set an alias to a command which doesn't exist!"
        try:
            self.db.add_command_alias(ctx.channel, existingCommand, alias)
            return f"Set new alias ({alias}) for ({existingCommand})!"
        except Exception as e:
            log.error(str(e))
            return "Failed to add alias."

    @command("broadcast")
    def bot_broadcast(self, ctx: CommandContext, data: str) -> str:
        if not ctx.author.is_admin:
            return "You ain't an admin you dingus!"
        data = data.strip()
        if not data:
            return "Usage: !alias <alias> <existingCommand>"
        # Communicate upward to the other nodes that we need
        # a broadcast.

        # TODO: disable this on discord.
        self.outputQueue.put(
            ShardUpdate(status="", message="", requestedBroadcast=data)
        )

        return "Broadcast sent!"
