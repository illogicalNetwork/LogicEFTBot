from __future__ import annotations  # type: ignore
import requests
import requests.utils
from requests.utils import quote  # type: ignore
from typing import Optional, Tuple
from common.config import settings
from common.models import (
    EFTLiveStats,
    KappaItemsModel,
    KappaQuestsModel,
    LogicalArmorModel,
    LogicalHelmetModel,
    MedicalModel,
    TarkovMarketModel,
    TarkovStatusModel,
    TarkovTimeModel,
    TraderResetsModel,
    TarkovChangesAmmoModel,
    TarkovChangesBanned,
    TarkovChangesMaps,
)
import math


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
    def check_astat(lang: str, query: str) -> TarkovChangesAmmoModel:
        astat_link = (
            settings["astat_link"][lang] if lang in settings["astat_link"] else None
        )
        if not astat_link:
            raise InvalidLocaleError(lang)
        crafted_url = astat_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovChangesAmmoModel.fromJSONObj(response)

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
    def tarkovStatus(lang: str, query: str) -> TarkovStatusModel:
        tarkovStatus_link = (
            settings["tarkovStatus_link"][lang]
            if lang in settings["tarkovStatus_link"]
            else None
        )
        if not tarkovStatus_link:
            raise InvalidLocaleError(lang)
        crafted_url = tarkovStatus_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovStatusModel.fromJSONObj(response)

    @staticmethod
    def check_maps(lang: str, query: str) -> TarkovChangesMaps:
        maps_link = (
            settings["maps_link"][lang] if lang in settings["maps_link"] else None
        )
        if not maps_link:
            raise InvalidLocaleError(lang)
        crafted_url = maps_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovChangesMaps.fromJSONObj(response)

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

    @staticmethod
    def check_tax(
        lang: str, requestValue: int, query: str
    ) -> Optional[Tuple[int, TarkovMarketModel]]:
        """
        Returns the computed tax, or None if there was an error.
        """
        price = EFT.check_price(lang, query)
        if not price:
            return None
        offerModifier = math.log10(float(price.basePrice) / requestValue)
        requestModifier = math.log10(requestValue / float(price.basePrice))
        if requestValue >= price.basePrice:
            requestModifier = pow(requestModifier, 1.08)
        else:
            offerModifier = pow(offerModifier, 1.08)
        tax = price.basePrice * 0.05 * pow(
            4, offerModifier
        ) + requestValue * 0.19 * pow(4, requestModifier)
        return (math.floor(tax), price)

    @staticmethod
    def traderResets(lang: str, query: str) -> TraderResetsModel:
        traderResets_link = (
            settings["tarkovtraders_link"][lang]
            if lang in settings["tarkovtraders_link"]
            else None
        )
        if not traderResets_link:
            raise InvalidLocaleError(lang)
        crafted_url = traderResets_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TraderResetsModel.fromJSONObj(response)

    @staticmethod
    def tarkovTime(lang: str, query: str) -> TarkovTimeModel:
        tarkovTime_link = (
            settings["tarkovTime_link"][lang]
            if lang in settings["tarkovTime_link"]
            else None
        )
        if not tarkovTime_link:
            raise InvalidLocaleError(lang)
        crafted_url = tarkovTime_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovTimeModel.fromJSONObj(response)

    @staticmethod
    def check_banned(lang: str, query: str) -> TarkovChangesBanned:
        banned_link = (
            settings["banned_link"][lang] if lang in settings["banned_link"] else None
        )
        if not banned_link:
            raise InvalidLocaleError(lang)
        crafted_url = banned_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return TarkovChangesBanned.fromJSONObj(response)

    @staticmethod
    def check_status(lang: str, query: str) -> EFTLiveStats:
        banned_link = (
            settings["eft_link"][lang] if lang in settings["eft_link"] else None
        )
        if not banned_link:
            raise InvalidLocaleError(lang)
        crafted_url = banned_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return EFTLiveStats.fromJSONObj(response)
