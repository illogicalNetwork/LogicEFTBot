from typing import Optional, Any
import requests
from inspect import signature
from bot.base import LogicEFTBotBase, command, CommandContext, AuthorInfo
from bot.eft import EFT
from bot.database import Database
from bot.log import log
from bot.config import settings, localized_string
import maya

# TODO: Move most of the actual API calls to eft.py (or move them all back into here)
class LogicEFTBot(LogicEFTBotBase):
    
    @command("armor")
    def bot_armor(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            armor = EFT.check_armor(lang, data)
            response = localized_string(
                lang,
                "twitch_armor",
                armor.armorName,
                armor.armorClass,
                armor.armorDurability,
                armor.armorZones,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("armorstats")
    def bot_armorstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            armor = EFT.check_armor(lang, data)
            response = localized_string(
                lang,
                "twitch_armorstats",
                armor.armorName,
                armor.effectiveDurability,
                armor.armorMoveSpeed,
                armor.armorTurnSpeed,
                armor.armorErgo,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("astat")
    def bot_astat(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            astat = EFT.check_astat(lang, data)
            response = localized_string(
                lang,
                "twitch_astat",
                astat.name,
                astat.damage,
                astat.penetration,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("avg7d")
    def bot_avg7d(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            avg7d = EFT.check_price(lang, data)
            response = localized_string(
                lang,
                "twitch_avg7d",
                avg7d.name,
                format(int(avg7d.avg7daysPrice),","),
                maya.MayaDT.from_datetime(avg7d.updated).slang_time(),
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("avg24h")
    def bot_avg24h(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            avg24h = EFT.check_price(lang, data)
            response = localized_string(
                lang,
                "twitch_avg24h",
                avg24h.name,
                format(int(avg24h.avg24hPrice),","),
                maya.MayaDT.from_datetime(avg24h.updated).slang_time(),
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("helmet")
    def bot_helmet(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            helmet = EFT.check_helmets(lang, data)
            response = localized_string(
                lang,
                "twitch_helmet",
                helmet.name,
                helmet.armorClass,
                helmet.armorDurability,
                helmet.armorRico,
                helmet.armorZones,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("helmetstats")
    def bot_helmetstats(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            helmet = EFT.check_helmets(lang, data)
            response = localized_string(
                lang,
                "twitch_helmetstats",
                helmet.name,
                helmet.armorMoveSpeed,
                helmet.armorTurnSpeed,
                helmet.armorErgo,
                helmet.helmetSoundReduc,
                helmet.helmetBlocksHeadset,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("kappaitem")
    def bot_kappaitem(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            kappa = EFT.check_kappaitem(lang, data)
            response = localized_string(
                lang,
                "twitch_kappaItems",
                kappa.quantity,
                kappa.name,                
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("kappaquest")
    def bot_kappaquest(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            kappa = EFT.check_kappaquests(lang, data)
            response = localized_string(
                lang,
                "twitch_kappaQuests",
                kappa.isReq,
                kappa.name,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response

    @command("medical")
    def bot_medical(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        try:
            medical = EFT.check_medical(lang, data)
            response = localized_string(
                lang,
                "twitch_medical",
                medical.name,
                medical.useTime,
                medical.resources,
                medical.resourceRate,
            )
            return response
        except:
            response = localized_string(
                lang,
                "searchFailed",
            )
            return response
            
    @command("profit")
    def bot_profit(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        response = localized_string(
        lang,
        "twitch_profit",
        )
        return response

    @command("price", "p")
    def bot_price(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        price = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "twitch_price",
            price.name,
            format(int(price.price),","),
            maya.MayaDT.from_datetime(price.updated).slang_time(),
        )
        return response

    @command("trader")
    def bot_trader(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        trader = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "twitch_trader",
            trader.name,
            trader.traderName,
            format(int(trader.traderPrice),","),
            maya.MayaDT.from_datetime(trader.updated).slang_time(),
        )
        return response

    @command("slot")
    def bot_slot(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        slot = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "twitch_slot",
            slot.name,
            format(int((slot.price / slot.slots)),",")
        )
        return response

    @command("wiki")
    def bot_wiki(self, ctx: CommandContext, data: str) -> str:
        log.info("%s - searching for %s\n", ctx.channel, data)
        lang = self.db.get_lang(ctx.channel)
        wiki = EFT.check_price(lang, data)
        response = localized_string(
            lang,
            "twitch_wiki",
            wiki.name,
            wiki.wikiLink
        )
        return response

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
