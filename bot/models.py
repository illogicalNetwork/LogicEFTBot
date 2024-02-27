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
        item = object['results'][0]
        return TCArmorModel(
            bsgID=item.get("Item ID"),
            armorName=item.get("Name"),
            armorClass=item.get("Armor Class"),
            armorType=item.get("Armor Type"),
            armorMaterial=item.get("Materials"),
            armorDurability=item.get("Max Durability"),
            armorMoveSpeed=item.get("Movement Speed Penalty"),
            armorTurnSpeed=item.get("Turn Speed Penalty"),
            armorErgo=item.get("Ergonomics Penalty"),
            armorEffectiveDurability=item.get("Effective Durability"),
            description=item.get("Description"),
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
        item = object['results'][0]
        return TCHelmetModel(
            bsgID=item.get("bsgID"),
            name=item.get("Name"),
            armorClass=item.get("Armor Class"),
            armorMoveSpeed=item.get("Movement Speed Penalty"),
            armorTurnSpeed=item.get("Turn Speed Penalty"),
            armorErgo=item.get("Ergonomics Penalty"),
            helmetBlocksHeadset=item.get("Blocks Earpiece"),
            description=item.get("Description"),
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
        item = object['results'][0]
        return TarkovMarketModel(
            name=item.get("name"),
            shortName=item.get("shortName"),
            price=item.get("price"),
            basePrice=item.get("basePrice"),
            avg24hPrice=item.get("avg24hPrice"),
            avg7daysPrice=item.get("avg7daysPrice"),
            traderName=item.get("traderName"),
            traderPrice=item.get("traderPrice"),
            updated=maya.parse(item.get("updated")).datetime(),
            slots=item.get("slots"),
            img=item.get("img"),
            wikiLink=item.get("wikiLink"),
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
        item = object['results'][0]
        return TCAmmoModel(
            bsgID=item.get("Item ID"),
            name=item.get("Name"),
            description=item.get("Description"),
            damage=item.get("Flesh Damage"),
            penetration=item.get("Penetration Power"),
            armorDamage=item.get("Armor Damage"),
            fragmentation=item.get("Frag Chance"),
            accuracy=item.get("Accuracy"),
            recoil=item.get("Recoil"),
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
        item = object['results'][0]
        return TCMapsModel(
            name=object.get("Name"),
            duration=item.get("Raid Timer"),
            minCount=item.get("Min Players"),
            maxCount=item.get("Max Players"),
            shortName=item.get("Map Internal Name"),
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