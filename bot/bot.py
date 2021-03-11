from typing import Optional, Any
import requests
from inspect import signature
from bot.base import LogicEFTBotBase, command, CommandContext, AuthorInfo
from bot.eft import EFT
from bot.models import (
    TarkovMarketModel,
    TarkovDatabaseModel,
    ArmorModel,
    HelmetModel,
    AmmoModel,
    safe_int,
)
from bot.database import Database
from bot.log import log
from bot.config import settings, localized_string


class LogicEFTBot(LogicEFTBotBase):
    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        armor = EFT.check_armor(lang, data)
        return armor

    @command("armorstats")
    def bot_armorstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        armorstats = EFT.check_armorstats(lang, data)
        return armorstats

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        astat = EFT.check_astat(lang, data)
        return astat

    @command("avg7d")
    def bot_avg7d(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        avg7d = EFT.check_avg7d(lang, data)
        return avg7d

    @command("avg24")
    def bot_avg24h(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        avg24h = EFT.check_avg24h(lang, data)
        return avg24h

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        helmet = EFT.check_helmets(lang, data)
        return helmet

    @command("helmetstats")
    def bot_helmetstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        helmetstats = EFT.check_helmetstats(lang, data)
        return helmetstats

    @command("kappaitem")
    def bot_kappaitem(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        kappaitem = EFT.check_kappaitem(lang, data)
        return kappaitem

    @command("kappaquest")
    def bot_kappaquest(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        kappaquest = EFT.check_kappaquest(lang, data)
        return kappaquest

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        medical = EFT.check_medical(lang, data)
        return medical

    @command("profit")
    def bot_profit(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        profit = EFT.check_profit(lang, data)
        return profit

    @command("price", "p")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        price = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "price",
            price.name,
            price.price,
            price.updated.strftime("%m/%d/%Y %H:%M:%S"),
        )
        return response

    @command("trader")
    def bot_trader(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        trader = EFT.check_trader(lang, data)
        return trader

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        slot = EFT.check_slot(lang, data)
        return slot

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        wiki = EFT.check_wiki(lang, data)
        return wiki

    @command("eftbot")
    def eft_bot(self, ctx: CommandContext, _=None) -> str:
        return localized_string(self.db.get_lang(ctx.channel), "botHelp")

    @command("help")
    def bot_help(self, ctx: CommandContext, _=None) -> str:
        return localized_string(self.db.get_lang(ctx.channel), "botHelp")

    @command("addbot")
    def bot_add_bot(
        self, ctx: CommandContext, _=None
    ) -> str:  # Later change this to invite link
        return localized_string(self.db.get_lang(ctx.channel), "addBot")

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

    @command("tax")
    def calculate_tax(self, ctx: CommandContext, data: str) -> str:
        lang = self.db.get_lang(ctx.channel)
        tax_link = settings.get("tax_link", {}).get(lang, None)
        USAGE = "Usage: !tax <amount> <item> - Compute the tax incurred when selling <item> for <amount> roubles on the flea market."
        if not data:
            return USAGE
        parts = data.split()
        if len(parts) < 2:
            return localized_string(lang, "invalid_command_tax_link")
        amount = safe_int(parts[0], 0)
        if amount == 0:
            return USAGE
        query = " ".join(parts[1:])
        tax_amount = EFT.check_tax(lang, amount, query)
        if not tax_amount:
            return USAGE
        (tax, model) = tax_amount
        return localized_string(
            lang,
            "calculateTax",
            model.name,
            tax,
            model.updated.strftime("%m/%d/%Y %H:%M:%S"),
        )
