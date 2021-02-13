
from typing import Optional, Any
import requests
from inspect import signature
from bot.base import LogicEFTBotBase, command, CommandContext, AuthorInfo
from bot.eft import EFT
from bot.database import Database
from bot.log import log
from bot.config import settings, localized_string

# TODO: Move most of the actual API calls to eft.py (or move them all back into here)
class LogicEFTBot(LogicEFTBotBase):

    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        armor = EFT.check_armor(lang, data)
        return armor

    @command("armorstats")
    def bot_armorstats(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        armorstats = EFT.check_armorstats(lang, data)
        return armorstats

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        helmet = EFT.check_helmets(lang, data)
        return helmet

    @command("helmetstats")
    def bot_helmetstats(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        helmetstats = EFT.check_helmetstats(lang, data)
        return helmetstats

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        astat = EFT.check_astat(lang, data)
        return astat

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        medical = EFT.check_medical(lang, data)
        return medical

    @command("price")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        price = EFT.check_price(lang, data)
        return price
    
    @command("trader")
    def bot_trader(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        trader = EFT.check_trader(lang, data)
        return trader

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        slot = EFT.check_slot(lang, data)
        return slot

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = Database.get().get_lang(ctx.channel)
        wiki = EFT.check_wiki(lang, data)
        return wiki

    @command("eftbot")
    def eft_bot(self, ctx: CommandContext, _=None) -> str:
        return localized_string(Database.get().get_lang(ctx.channel), "botHelp")

    @command("help")
    def bot_help(self, ctx: CommandContext, _=None) -> str:
        return localized_string(Database.get().get_lang(ctx.channel), "botHelp")

    @command("addbot")
    def bot_add_bot(self, ctx: CommandContext, _=None) -> str: #Later change this to invite link
        return localized_string(Database.get().get_lang(ctx.channel), "addBot")

    @command("setCD")
    def bot_set_cd(self, ctx: CommandContext, cooldown_time=settings["default_cooldown"]) -> str:
        if not ctx.author.is_mod:
            # TODO: unlocalized string.
            return "You ain't a mod you dingus!"
        Database.get().update_cooldown(ctx.channel, cooldown_time)
        return "Cooldown has been set to {}".format(cooldown_time)

    @command("setLang")
    def bot_set_lang(self, ctx: CommandContext, lang : str = settings["default_lang"]) -> str:
        if not ctx.author.is_mod:
            return "@" + ctx.author.name + " You ain't a mod you dingus!"
        Database.get().update_lang(ctx.channel, lang, ctx.channel)
        return "@" + ctx.author.name + ' - Language has been set to {}'.format(lang)
