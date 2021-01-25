
from typing import Optional, Any
import requests
from inspect import signature
from .base import LogicEFTBotBase, command, CommandContext, AuthorInfo
from .eft import EFT
from .database import db
from .log import log
from .config import settings, locale

# TODO: Move most of the actual API calls to eft.py (or move them all back into here)
class LogicEFTBot(LogicEFTBotBase):

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        astat = EFT.check_astat(lang, data)
        return '@{} {}'.format(ctx.author.name, astat)

    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        armor = EFT.check_armor(lang, data)
        return '@{} {}'.format(ctx.author.name, armor)

    @command("armorstats")
    def bot_armorstats(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        armorstats = EFT.check_armorstats(lang, data)
        return '@{} {}'.format(ctx.author.name, armorstats)

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        helmet = EFT.check_helmets(lang, data)
        return '@{} {}'.format(ctx.author.name, helmet)

    @command("helmetstats")
    def bot_helmetstats(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        helmetstats = EFT.check_helmetstats(lang, data)
        return '@{} {}'.format(ctx.author.name, helmetstats)

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        medical = EFT.check_medical(lang, data)
        return '@{} {}'.format(ctx.author.name, medical)

    @command("price")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        price = EFT.check_price(lang, data)
        return '@{} {}'.format(ctx.author.name, price)

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        slot = EFT.check_slot(lang, data)
        return '@{} {}'.format(ctx.author.name, slot)

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        wiki = EFT.check_wiki(lang, data)
        return '@{} {}'.format(ctx.author.name, wiki)

    @command("eftbot")
    def eft_bot(self, ctx: CommandContext, _=None) -> str:
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["botHelp"])

    @command("help")
    def bot_help(self, ctx: CommandContext, _=None) -> str:
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["botHelp"])

    @command("addbot")
    def bot_add_bot(self, ctx: CommandContext, _=None) -> str: #Later change this to invite link
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["addBot"])

    @command("setcd")
    def bot_set_cd(self, ctx: CommandContext, cooldown_time=settings["default_cooldown"]) -> str:
        if not ctx.author.is_mod:
            # TODO: unlocalized string.
            return "@" + ctx.author.name + " You ain't a mod you dingus!"
        db.update_cooldown(ctx.channel, cooldown_time)
        return "@" + ctx.author.name + ' - Cooldown has been set to {}'.format(cooldown_time)

    @command("setlang")
    def bot_set_lang(self, ctx: CommandContext, lang : str = settings["default_lang"]) -> str:
        if not ctx.author.is_mod:
            return "@" + ctx.author.name + " You ain't a mod you dingus!"
        if lang not in locale.keys():
            return "@" + ctx.author.name + " Not a valid option, try " + str(locale.keys())
        db.update_lang(ctx.channel, lang, ctx.channel)
        return "@" + ctx.author.name + ' - Language has been set to {}'.format(lang)
