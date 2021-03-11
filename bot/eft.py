from __future__ import annotations  # type: ignore
import requests
import requests.utils
from requests.utils import quote  # type: ignore
from typing import Optional, Any
from bot.config import settings
from bot.models import (
    TarkovMarketModel,
    WikiAmmoModel,
    LogicalArmorModel,
    LogicalHelmetModel,
    MedicalModel,
    kappaItemsModel,
    kappaQuestsModel,
)
from dataclasses import dataclass
import datetime
import maya
import json


class InvalidLocaleError(Exception):
    def __init__(self, locale):
        super().__init__(f"Unknown locale {locale}")
        self.locale = locale


# utility class for interfacing with EFT's data.
class EFT:
    @staticmethod
    def check_armor(lang: str, query: str) -> LogicalArmorModel:
        armor_link = (
            settings["armor_link"][lang] if lang in settings["armor_link"] else None
        )
        if not armor_link:
            raise InvalidLocaleError(lang)
        crafted_url = armor_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return LogicalArmorModel.fromJSONObj(response)

    @staticmethod
    def check_astat(lang: str, query: str) -> WikiAmmoModel:
        astat_link = (
            settings["astat_link"][lang] if lang in settings["astat_link"] else None
        )
        if not astat_link:
            raise InvalidLocaleError(lang)
        crafted_url = astat_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return WikiAmmoModel.fromJSONObj(response)

    @staticmethod
    def check_helmets(lang: str, query: str) -> LogicalHelmetModel:
        helmet_link = (
            settings["helmet_link"][lang] if lang in settings["helmet_link"] else None
        )
        if not helmet_link:
            raise InvalidLocaleError(lang)
        crafted_url = helmet_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return LogicalHelmetModel.fromJSONObj(response)

    @staticmethod
    def check_kappaquests(lang: str, query: str) -> KappaQuestsModel:
        kappaquests_link = (
            settings["kappaquests_link"][lang]
            if lang in settings["kappaquests_link"]
            else None
        )
        if not kappaquests_link:
            raise InvalidLocaleError(lang)
        crafted_url = kappaquests_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return KappaQuestsModel.fromJSONObj(response)

    @staticmethod
    def check_kappaitem(lang: str, query: str) -> KappaItemsModel:
        kappaitem_link = (
            settings["kappaitem_link"][lang]
            if lang in settings["kappaitem_link"]
            else None
        )
        if not kappaitem_link:
            raise InvalidLocaleError(lang)
        crafted_url = kappaitem_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return KappaItemsModel.fromJSONObj(response)

    @staticmethod
    def check_medical(lang: str, query: str) -> MedicalModel:
        medical_link = (
            settings["medical_link"][lang] if lang in settings["medical_link"] else None
        )
        if not medical_link:
            raise InvalidLocaleError(lang)
        crafted_url = medical_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return MedicalModel.fromJSONObj(response)

    @staticmethod
    def check_price(lang: str, query: str) -> TarkovMarketModel:
        price_link = (
            settings["price_link"][lang] if lang in settings["price_link"] else None
        )
        if not price_link:
            raise InvalidLocaleError(lang)
        crafted_url = price_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovMarketModel.fromJSONObj(response)
