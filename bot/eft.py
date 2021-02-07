#!/usr/bin/python3
import requests
import requests.utils
from requests.utils import quote # type: ignore
from typing import Optional
from bot.config import settings

class InvalidLocaleError(Exception):
    def __init__(self, locale):
        super().__init__(f"Unknown locale {locale}")
        self.locale = locale
# utility class for interfacing with EFT's data.
class EFT:

    @staticmethod
    def check_astat(lang: str, query: str) -> str:
        ammo_link = settings["ammo_link"][lang] if lang in settings["ammo_link"] else None
        if not ammo_link:
            raise InvalidLocaleError(lang)
        crafted_url = ammo_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_armor(lang: str, query: str) -> str:
        armor_link = settings["armor_link"][lang] if lang in settings["armor_link"] else None
        if not armor_link:
            raise InvalidLocaleError(lang)
        crafted_url = armor_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_armorstats(lang: str, query: str) -> str:
        armorstats_link = settings["armorstats_link"][lang] if lang in settings["armorstats_link"] else None
        if not armorstats_link:
            raise InvalidLocaleError(lang)
        crafted_url = armorstats_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()\

    @staticmethod
    def check_helmets(lang: str, query: str) -> str:
        helmet_link = settings["helmet_link"][lang] if lang in settings["helmet_link"] else None
        if not helmet_link:
            raise InvalidLocaleError(lang)
        crafted_url = helmet_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_helmetstats(lang: str, query: str) -> str:
        helmetstats_link = settings["helmetstats_link"][lang] if lang in settings["helmetstats_link"] else None
        if not helmetstats_link:
            raise InvalidLocaleError(lang)
        crafted_url = helmetstats_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_medical(lang: str, query: str) -> str:
        medical_link = settings["medical_link"][lang] if lang in settings["medical_link"] else None
        if not medical_link:
            raise InvalidLocaleError(lang)
        crafted_url = medical_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_price(lang: str, query: str) -> str:
        price_link = settings["price_link"][lang] if lang in settings["price_link"] else None
        if not price_link:
            raise InvalidLocaleError(lang)
        crafted_url = price_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_slot(lang: str, query: str) -> str:
        slot_link = settings["slot_link"][lang] if lang in settings["slot_link"] else None
        if not slot_link:
            raise InvalidLocaleError(lang)
        crafted_url = slot_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_wiki(lang: str, query: str) -> str:
        wiki_link = settings["wiki_link"][lang] if lang in settings["wiki_link"] else None
        if not wiki_link:
            raise InvalidLocaleError(lang)
        crafted_url = wiki_link.format(quote(query))
        response = requests.get(crafted_url).text
        return response.strip()
