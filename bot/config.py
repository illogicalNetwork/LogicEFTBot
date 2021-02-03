import json
import io
from typing import Dict, Any

settings : Dict[str, Any] = {}
# Load JSON settings file.
with open("settings.json", "r") as __f:
    settings = json.load(__f)

locale: Dict[str, Dict[str, str]] = {}
with io.open("localizations.json", "r", encoding="utf-8") as _f:
    locale = json.load(_f)

def localized_string(lang: str, string: str) -> str:
    return str(locale[lang][string])
