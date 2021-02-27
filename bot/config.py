import json
import io
import os
from typing import Dict, Any

settings: Dict[str, Any] = {}
# Load JSON settings file.
with open("settings.json", "r") as __f:
    settings = json.load(__f)

locale: Dict[str, Dict[str, str]] = {}
with io.open("localizations.json", "r", encoding="utf-8") as _f:
    locale = json.load(_f)

BOT_UI_ENABLED = bool(os.environ.get("BOT_UI_ENABLED", None))


def localized_string(lang: str, string: str, *args: str) -> str:
    resp = str(locale[lang][string])
    if args:
        resp = resp.format(*args)
    return resp
