from __future__ import annotations  # type: ignore
import requests
import requests.utils
from requests.utils import quote  # type: ignore
from typing import Optional, Any
from bot.config import settings
from dataclasses import dataclass


class InvalidLocaleError(Exception):
    def __init__(self, locale):
        super().__init__(f"Unknown locale {locale}")
        self.locale = locale


{"uid":"f64635c1-2f92-4797-ad00-702683d61c85","name":"LBT 6094A Slick Plate Carrier (80\/80)","shortName":"Slick","price":499999,"basePrice":374500,"avg24hPrice":474105,"avg7daysPrice":477360,"traderName":"Ragman","traderPrice":232190,"traderPriceCur":"\u20bd","updated":"2021-02-25T04:24:07.544Z","slots":9,"diff24h":5.46,"diff7days":4.74,"icon":"","link":"https:\/\/tarkov-market.com\/item\/lbt_6094a_slick_plate_carrier","wikiLink":"https:\/\/escapefromtarkov.gamepedia.com\/LBT_6094A_Slick_Plate_Carrier","img":"https:\/\/gamepedia.cursecdn.com\/escapefromtarkov_gamepedia\/3\/38\/Slick_Icon.png?version=3dd2b4822b9bf88a1dd712fdb8ab002f","imgBig":"https:\/\/gamepedia.cursecdn.com\/escapefromtarkov_gamepedia\/thumb\/6\/65\/LBT_6094A_Slick_Plate_Carrier.png\/640px-LBT_6094A_Slick_Plate_Carrier.png?version=a90d49fe91229a197342aa4079f26ea9","bsgId":"5e4abb5086f77406975c9342","isFunctional":true,"reference":"https:\/\/www.patreon.com\/tarkov_market"}

def safe_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except:
        return fallback

@dataclass
class PriceResponseModel:
    name: str
    shortName: str
    price: int
    basePrice: int
    avg24hPrice: int
    avg7daysPrice: int
    traderName: str
    traderPrice: int
    tracePriceCur: str
    updated: datetime
    slots: int
    img: str
    imgBig: str

    @staticmethod
    def fromJSONObj(cls, json: Any) -> PriceResponseModel:
        return PriceResponseModel(
            name=json.get('name'),
            shortName=json.get('shortName'),
            price=safe_int(json.get('price'), 0),
            basePrice=safe_int(json.get('basePrice'), 0),
            avg24hPrice=safe_int(json.get('avg24hPrice'), 0),
            avg7daysPrice=safe_int(json.get('avg7daysPrice'), 0),
            traderName=json.get('traderName'),
            traderPrice=safe_int(json.get('traderPrice'), 0),
            tracePriceCur=json.get('tracePriceCur'),
            updated=maya.parse(safe_int(json.get('updated'), 0)).datetime(),
            slots=safe_int(json.get('slots'), 0),
            img=json.get('img'),
            imgBig=json.get('imgBig')
        )




# utility class for interfacing with EFT's data.
class EFT:
    @staticmethod
    def check_armor(lang: str, query: str) -> str:
        armor_link = (
            settings["armor_link"][lang] if lang in settings["armor_link"] else None
        )
        if not armor_link:
            raise InvalidLocaleError(lang)
        crafted_url = armor_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_armorstats(lang: str, query: str) -> str:
        armorstats_link = (
            settings["armorstats_link"][lang]
            if lang in settings["armorstats_link"]
            else None
        )
        if not armorstats_link:
            raise InvalidLocaleError(lang)
        crafted_url = armorstats_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_astat(lang: str, query: str) -> str:
        ammo_link = (
            settings["ammo_link"][lang] if lang in settings["ammo_link"] else None
        )
        if not ammo_link:
            raise InvalidLocaleError(lang)
        crafted_url = ammo_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_avg7d(lang: str, query: str) -> str:
        avg7d_link = (
            settings["avg7d_link"][lang] if lang in settings["avg7d_link"] else None
        )
        if not avg7d_link:
            raise InvalidLocaleError(lang)
        crafted_url = avg7d_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_avg24h(lang: str, query: str) -> str:
        avg24h_link = (
            settings["avg24h_link"][lang] if lang in settings["avg24h_link"] else None
        )
        if not avg24h_link:
            raise InvalidLocaleError(lang)
        crafted_url = avg24h_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_helmets(lang: str, query: str) -> str:
        helmet_link = (
            settings["helmet_link"][lang] if lang in settings["helmet_link"] else None
        )
        if not helmet_link:
            raise InvalidLocaleError(lang)
        crafted_url = helmet_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_helmetstats(lang: str, query: str) -> str:
        helmetstats_link = (
            settings["helmetstats_link"][lang]
            if lang in settings["helmetstats_link"]
            else None
        )
        if not helmetstats_link:
            raise InvalidLocaleError(lang)
        crafted_url = helmetstats_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_medical(lang: str, query: str) -> str:
        medical_link = (
            settings["medical_link"][lang] if lang in settings["medical_link"] else None
        )
        if not medical_link:
            raise InvalidLocaleError(lang)
        crafted_url = medical_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_profit(lang: str, query: str) -> str:
        profit_link = (
            settings["profit_link"][lang] if lang in settings["profit_link"] else None
        )
        if not profit_link:
            raise InvalidLocaleError(lang)
        crafted_url = profit_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_price(lang: str, query: str) -> PriceResponseModel:
        price_link = (
            settings["price_link"][lang] if lang in settings["price_link"] else None
        )
        if not price_link:
            raise InvalidLocaleError(lang)
        crafted_url = price_link.format(quote(query), quote(lang))
        response = requests.get(crafted_url).json()
        return PriceResponseModel.fromJSONObj(response)

    @staticmethod
    def check_slot(lang: str, query: str) -> str:
        slot_link = (
            settings["slot_link"][lang] if lang in settings["slot_link"] else None
        )
        if not slot_link:
            raise InvalidLocaleError(lang)
        crafted_url = slot_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_trader(lang: str, query: str) -> str:
        trader_link = (
            settings["trader_link"][lang] if lang in settings["trader_link"] else None
        )
        if not trader_link:
            raise InvalidLocaleError(lang)
        crafted_url = trader_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_wiki(lang: str, query: str) -> str:
        wiki_link = (
            settings["wiki_link"][lang] if lang in settings["wiki_link"] else None
        )
        if not wiki_link:
            raise InvalidLocaleError(lang)
        crafted_url = wiki_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()
