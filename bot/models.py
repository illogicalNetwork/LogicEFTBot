from __future__ import annotations  # type: ignore
import requests
import requests
import requests.utils
import requests.utils
from requests.utils import quote  # type: ignore
from requests.utils import quote  # type: ignore
from typing import Optional
from typing import Optional, Any
from bot.config import settings
from bot.config import settings
from dataclasses import dataclass
import datetime
import maya
import json

def safe_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except:
        return fallback


@dataclass
class TarkovMarketModel:
    name: str
    shortName: str
    price: int
    basePrice: int
    avg24hPrice: int
    avg7daysPrice: int
    traderName: str
    traderPrice: int
    tracePriceCur: str
    updated: datetime.datetime
    slots: int
    img: str
    imgBig: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovMarketModel:
        return TarkovMarketModel(
            name=object.get("name"),
            shortName=object.get("shortName"),
            price=safe_int(object.get("price"), 0),
            basePrice=safe_int(object.get("basePrice"), 0),
            avg24hPrice=safe_int(object.get("avg24hPrice"), 0),
            avg7daysPrice=safe_int(object.get("avg7daysPrice"), 0),
            traderName=object.get("traderName"),
            traderPrice=safe_int(object.get("traderPrice"), 0),
            tracePriceCur=object.get("tracePriceCur"),
            updated=maya.parse(object.get("updated")).datetime(),
            slots=safe_int(object.get("slots"), 0),
            img=object.get("img"),
            imgBig=object.get("imgBig"),
        )

@dataclass
class TarkovDatabaseModel:
    name: str
    shortName: str
    description: str
    useTime: int
    effects: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovDatabaseModel:
        return TarkovDatabaseModel(
            name=object.get("name"),
            shortName=object.get("shortName"),
            description=object.get("description"),
            useTime=object.get("useTime"),
            effects=object.get("effects"),
        )

@dataclass
class HelmetModel:
    name: str
    helmetsclass: int
    zones: str
    dura: int
    rico: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> HelmetModel:
        return HelmetModel(
            name=object.get("name"),
            helmetsclass=object.get("helmetsclass"),
            zones=object.get("zones"),
            dura=object.get("dura"),
            rico=object.get("rico"),
        )

@dataclass
class ArmorModel:
    name: str
    armorclass: int
    zones: str
    dura: int
    materials: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> ArmorModel:
        return ArmorModel(
            name=object.get("name"),
            armorclass=object.get("armorclass"),
            zones=object.get("zones"),
            dura=object.get("dura"),
            materials=object.get("materials"),
        )

@dataclass
class AmmoModel:
    name: str
    flesh: int
    pen: int
    armor: int
    accuracy: int
    recoil: int
    frag:int
    img: str
    url: str
    desc: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> AmmoModel:
        return AmmoModel(
            name=object.get("name"),
            flesh=object.get("flesh"),
            pen=object.get("pen"),
            armor=object.get("armor"),
            accuracy=object.get("accuracy"),
            recoil=object.get("recoil"),
            frag=object.get("frag"),         
            img=object.get("img"),
            url=object.get("wikiURL"),
            desc=object.get("desc"),
        )