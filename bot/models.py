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
class LogicalHelmetModel:
    name: str
    helmetsclass: int
    zones: str
    dura: int
    rico: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> LogicalHelmetModel:
        return LogicalHelmetModel(
            name=object.get("name"),
            helmetsclass=object.get("helmetsclass"),
            zones=object.get("zones"),
            dura=object.get("dura"),
            rico=object.get("rico"),
        )

@dataclass
class LogicalArmorModel:
    name: str
    armorZones: str
    armorclass: str
    material: str
    armorDurability: str
    armorMoveSpeed: str
    armorTurnSpeed: str
    ergo: str
    effectiveDurability: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> LogicalArmorModel:
        return LogicalArmorModel(
            name=object.get("name"),
            armorZones=object.get("armorZones"),
            armorclass=object.get("armorclass"),
            material=object.get("material"),
            armorDurability=object.get("durability"),
            armorMoveSpeed=object.get("moveSpeed"),
            armorTurnSpeed=object.get("turnSpeed"),
            armorErgo=object.get("ergo"),
            effectiveDurability=object.get("effectiveDurability"),
        )

@dataclass
class TarkovDatabaseMedicalModel:
    name: str
    shortName: str
    description: str
    useTime: int
    effects: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovDatabaseMedicalModel:
        return TarkovDatabaseMedicalModel(
            name=object.get("name"),
            shortName=object.get("shortName"),
            description=object.get("description"),
            useTime=object.get("useTime"),
            effects=object.get("effects"),
        )

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
    updated: datetime.datetime
    slots: int
    img: str
    wikiLink: str

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
            updated=maya.parse(object.get("updated")).datetime(),
            slots=safe_int(object.get("slots"), 0),
            img=object.get("img"),
            wikiLink=object.get("wikiLink"),
        )

@dataclass
class WikiAmmoModel:
    bsgID: str
    name: str
    description: str
    damage: int
    penetration: int
    armorDamage: int
    fragmentation: str
    accuracy: str
    recoil: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> WikiAmmoModel:
        return WikiAmmoModel(
            bsgID=object.get("_id"),
            name=object.get("name"),
            description=object.get("description"),
            damage=object.get("damage"),
            penetration=object.get("penetration"),
            armorDamage=object.get("armorDamage"),
            fragmentation=object.get("fragmentation").get("chance"),
            accuracy=object.get("weaponModifier").get("accuracy"),
            recoil=object.get("weaponModifier").get("recoil"),
        )