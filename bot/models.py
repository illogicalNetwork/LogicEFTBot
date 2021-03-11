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


@dataclass
class KappaItemsModel:
    name: str
    quantity: int

    @classmethod
    def fromJSONObj(cls, object: Any) -> KappaItemsModel:
        return KappaItemsModel(
            name=object.get("name"),
            quantity=object.get("itemQTY"),
        )


@dataclass
class KappaQuestsModel:
    name: str
    isReq: int

    @classmethod
    def fromJSONObj(cls, object: Any) -> KappaQuestsModel:
        return KappaQuestsModel(
            name=object.get("name"),
            isReq=object.get("kappaReq"),
        )


@dataclass
class LogicalHelmetModel:
    bsgID: str
    name: str
    armorClass: str
    armorZones: str
    armorDurability: str
    armorRico: str
    armorMoveSpeed: str
    armorTurnSpeed: str
    armorErgo: str
    helmetSoundReduc: str
    helmetBlocksHeadset: str
    wikiLink: str
    description: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> LogicalHelmetModel:
        return LogicalHelmetModel(
            bsgID=object.get("bsgID"),
            name=object.get("name"),
            armorClass=object.get("armorClass"),
            armorZones=object.get("armorZones"),
            armorDurability=object.get("dura"),
            armorRico=object.get("rico"),
            armorMoveSpeed=object.get("moveSpeed"),
            armorTurnSpeed=object.get("turnSpeed"),
            armorErgo=object.get("ergo"),
            helmetSoundReduc=object.get("soundsReduc"),
            helmetBlocksHeadset=object.get("blocksHeadset"),
            wikiLink=object.get("wikiLink"),
            description=object.get("description"),
        )


@dataclass
class LogicalArmorModel:
    bsgID: str
    armorName: str
    armorZones: str
    armorClass: str
    armorMaterial: str
    armorDurability: str
    armorMoveSpeed: str
    armorTurnSpeed: str
    armorErgo: str
    effectiveDurability: str
    wikiLink: str
    description: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> LogicalArmorModel:
        return LogicalArmorModel(
            bsgID=object.get("bsgID"),
            armorName=object.get("name"),
            armorZones=object.get("zones"),
            armorClass=object.get("armorclass"),
            armorMaterial=object.get("materials"),
            armorDurability=object.get("dura"),
            armorMoveSpeed=object.get("moveSpeed"),
            armorTurnSpeed=object.get("turnSpeed"),
            armorErgo=object.get("ergo"),
            effectiveDurability=object.get("effective"),
            wikiLink=object.get("wikiLink"),
            description=object.get("description"),
        )


@dataclass
class MedicalModel:
    bsgID: str
    name: str
    description: str
    useTime: int
    resources: int
    resourceRate: int
    wikiLink: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> MedicalModel:
        return MedicalModel(
            bsgID=object.get("bsgId"),
            name=object.get("name"),
            description=object.get("description"),
            useTime=object.get("useTime"),
            resources=object.get("resources"),
            resourceRate=object.get("resourceRate"),
            wikiLink=object.get("wikiLink"),
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
    wikiLink: str

    @classmethod
    def fromJSONObj(cls, object: Any) -> WikiAmmoModel:
        return WikiAmmoModel(
            bsgID=object.get("bsgId"),
            name=object.get("name"),
            description=object.get("description"),
            damage=object.get("damage"),
            penetration=object.get("penetration"),
            armorDamage=object.get("armorDamage"),
            fragmentation=object.get("fragChance"),
            accuracy=object.get("accuracy"),
            recoil=object.get("recoil"),
            wikiLink=object.get("wikiLink"),
        )
