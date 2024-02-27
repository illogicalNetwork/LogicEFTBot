from __future__ import annotations
import requests
import requests.utils
from requests.utils import quote
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
class TCArmorModel:
    bsgID: str
    armorName: str
    armorZones: str
    armorClass: str
    armorType: str
    armorMaterial: str
    armorDurability: str
    armorMoveSpeed: str
    armorTurnSpeed: str
    armorErgo: str
    armorEffectiveDurability: str
    description: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TCArmorModel:
        return TCArmorModel(
            bsgID=object.get("Item ID"),
            armorName=object.get("Name"),
            armorClass=object.get("Armor Class"),
            armorType=object.get("Armor Type"),
            armorMaterial=object.get("Materials"),
            armorDurability=object.get("Max Durability"),
            armorMoveSpeed=object.get("Movement Speed Penalty"),
            armorTurnSpeed=object.get("Turn Speed Penalty"),
            armorErgo=object.get("Ergonomics Penalty"),
            armorEffectiveDurability=object.get("Effective Durability"),
            description=object.get("Description"),
        )


@dataclass
class TCHelmetModel:
    bsgID: str
    name: str
    armorClass: str
    armorMoveSpeed: str
    armorTurnSpeed: str
    armorErgo: str
    helmetBlocksHeadset: str
    description: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TCHelmetModel:
        return TCHelmetModel(
            bsgID=object.get("bsgID"),
            name=object.get("Name"),
            armorClass=object.get("Armor Class"),
            armorMoveSpeed=object.get("Movement Speed Penalty"),
            armorTurnSpeed=object.get("Turn Speed Penalty"),
            armorErgo=object.get("Ergonomics Penalty"),
            helmetBlocksHeadset=object.get("Blocks Earpiece"),
            description=object.get("Description"),
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
        print(object)
        return TarkovMarketModel(
            name=object.get("name"),
            shortName=object.get("shortName"),
            price=object.get("price"),
            basePrice=object.get("basePrice"),
            avg24hPrice=object.get("avg24hPrice"),
            avg7daysPrice=object.get("avg7daysPrice"),
            traderName=object.get("traderName"),
            traderPrice=object.get("traderPrice"),
            updated=maya.parse(object.get("updated")).datetime(),
            slots=object.get("slots"),
            img=object.get("img"),
            wikiLink=object.get("wikiLink"),
        )


@dataclass
class TCAmmoModel:
    bsgID: str
    name: str
    description: str
    damage: int
    penetration: int
    armorDamage: int
    fragmentation: str
    accuracy: str
    recoil: str
    # wikiLink: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TCAmmoModel:
        return TCAmmoModel(
            bsgID=object.get("Item ID"),
            name=object.get("Name"),
            description=object.get("Description"),
            damage=object.get("Flesh Damage"),
            penetration=object.get("Penetration Power"),
            armorDamage=object.get("Armor Damage"),
            fragmentation=object.get("Frag Chance"),
            accuracy=object.get("Accuracy"),
            recoil=object.get("Recoil"),
            # wikiLink=object.get("wikiLink"),
        )


@dataclass
class TarkovStatusModel:
    name: str
    status: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovStatusModel:
        return TarkovStatusModel(
            name=object.get("name"),
            status=object.get("status"),
        )

@dataclass
class TarkovTimeModel:
    left: str
    right: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovTimeModel:
        return TarkovTimeModel(
            left=object.get("left"),
            right=object.get("right"),
        )


@dataclass
class TarkovChangesBanned:
    bsgID: str
    name: str
    banned: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TarkovChangesBanned:
        return TarkovChangesBanned(
            bsgID=object.get("bsgID"),
            name=object.get("Name"),
            banned=object.get("Can Sell on Flea"),
        )

@dataclass
class TCMapsModel:
    name: str
    duration: str
    minCount: str
    maxCount: str
    shortName: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> TCMapsModel:
        return TCMapsModel(
            name=object.get("Name"),
            duration=object.get("Raid Timer"),
            minCount=object.get("Min Players"),
            maxCount=object.get("Max Players"),
            shortName=object.get("Map Internal Name"),
        )
    
@dataclass
class EFTLiveStats:
    eft_version: str
    lobby_average: str
    highest_level_region: str
    highest_level_name: str
    highest_level: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> EFTLiveStats:
        return EFTLiveStats(
            eft_version=object.get("eft_version"),
            lobby_average=object.get("lobby_average"),
            highest_level_region=object.get("highest_level_region"),
            highest_level_name=object.get("highest_level_name"),
            highest_level=object.get("highest_level"),
        )