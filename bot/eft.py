#!/usr/bin/python3
import requests
from typing import Optional
from .config import settings

class InvalidLocaleError(Exception):
    def __init__(self, locale):
        super().__init__(f"Unknown locale {locale}")
        self.locale = locale

# utility class for interfacing with EFT's data.
class EFT:
    @staticmethod
    def check_price(lang: str, query: str) -> str:
        price_link = settings["price_link"][lang] if lang in settings["price_link"] else None
        if not price_link:
            raise InvalidLocaleError(lang)
        crafted_url = price_link + requests.utils.quote(query)
        response = requests.get(crafted_url).text
        return response.strip()

    @staticmethod
    def check_wiki(lang: str, query: str) -> str:
        wiki_link = settings["wiki_link"][lang] if lang in settings["wiki_link"] else None
        if not wiki_link:
            raise InvalidLocaleError(lang)
        crafted_url = wiki_link + requests.utils.quote(query)
        response = requests.get(crafted_url).text
        return response.strip()
