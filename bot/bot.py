
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
    @command("price")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        price = EFT.check_price(lang, data)
        log.info("Got price: %s", price)
        return '@{} {}'.format(ctx.author.name, price)

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info('%s - searching for %s\n', ctx.channel, data)
        lang = db.get_lang(ctx.channel)
        slot_link = settings["slot_link"][lang] if lang in settings["slot_link"] else None
        # TODO(security): Using user inputs in URL building like this is.. bad.
        # this needs to be sanitized.
        crafted_url = slot_link.format(data)
        response = requests.get(url = crafted_url).text
        return '@{} {}'.format(ctx.author.name, response)

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        lang = db.get_lang(ctx.channel)
        wiki = EFT.check_wiki(lang, data)
        return '@{} {}'.format(ctx.author.name, wiki)

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        lang = db.get_lang(ctx.channel)
        ammo_link = settings["ammo_link"][lang] if lang in settings["ammo_link"] else None
        crafted_url = ammo_link.format(data)
        response = requests.get(crafted_url).text
        return '@{} {}'.format(ctx.author.name, response)

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        lang = db.get_lang(ctx.channel)
        medical_link = settings["medical_link"][lang] if lang in settings["medical_link"] else None
        crafted_url = medical_link.format("{}".format(data))
        response = requests.get(crafted_url).text
        return '@{} {}'.format(ctx.author.name, response)

    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        lang = db.get_lang(ctx.channel)
        armor_link = settings["armor_link"][lang] if lang in settings["armor_link"] else None
        crafted_url = armor_link.format(data)
        response = requests.get(crafted_url).text
        return '@{} {}'.format(ctx.author.name, response)

    @command("eftbot")
    def eft_bot(self, ctx: CommandContext, _=None) -> str:
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["botHelp"])

    @command("help")
    def bot_help(self, ctx: CommandContext, _=None) -> str:
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["botHelp"])

    @command("addbot")
    def bot_add_bot(self, ctx: CommandContext, _=None) -> str: #Later change this to invite link
        return '@{} - {}'.format(ctx.author.name, locale[db.get_lang(ctx.channel)]["addBot"])

    @command("setCD")
    def bot_set_cd(self, ctx: CommandContext, cooldown_time=settings["default_cooldown"]) -> str:
        if not ctx.author.is_mod:
            # TODO: unlocalized string.
            return "@" + ctx.author.name + " You ain't a mod you dingus!"
        db.update_cooldown(ctx.channel, cooldown_time)
        return "@" + ctx.author.name + ' - Cooldown has been set to {}'.format(cooldown_time)

    @command("setLang")
    def bot_set_lang(self, ctx: CommandContext, lang : str = settings["default_lang"]) -> str:
        if not ctx.author.is_mod:
            return "@" + ctx.author.name + " You ain't a mod you dingus!"
        db.update_lang(ctx.channel, lang, ctx.channel)
        return "@" + ctx.author.name + ' - Language has been set to {}'.format(lang)
