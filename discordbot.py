import discord
from discord import app_commands
from bot.config import settings, localized_string
from bot.database import Database
from bot.eft import EFT
from bot.log import log
from bot.models import (
    safe_int,
)
import maya
import os

class LogicEFTClient(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        stream = discord.Streaming(platform="Twitch", name="/price & /tax » https://eft.bot", url="https://twitch.tv/TarkovChangesBot")
        await client.change_presence(activity=stream)
        await self.wait_until_ready()
        await tree.sync(guild=discord.Object(id=864750816082657301)) #force sync with tarkov-changes discord 
        if not self.synced: #check if slash commands have been synced 
            await tree.sync() #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")
        

client = LogicEFTClient()
tree = app_commands.CommandTree(client)
db = Database()

@tree.command(name = 'price', description='Check the price of an item via Tarkov-Market API') #guild specific slash command
async def price(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        price = EFT.check_price(lang, data)
        embed = discord.Embed(
            title=price.name,
            url=price.wikiLink,
            color=0x780A81,
        )
        embed.set_thumbnail(url=price.img)
        embed.add_field(
            name=localized_string(lang, "marketPrice"),
            value=format(int(price.price), ","),
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "marketTrader"),
            value=price.traderName,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "marketTraderPrice"),
            value=format(int(price.traderPrice), ","),
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "marketSlot"),
            value=format(round((price.price / price.slots)), ","),
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "market7dAvg"),
            value=format(int(price.avg7daysPrice), ","),
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "market24hAvg"),
            value=format(int(price.avg24hPrice), ","),
            inline=True,
        )
        embed.set_footer(
            text=localized_string(lang, "marketUpdated")
            + maya.MayaDT.from_datetime(price.updated).slang_time()
            + " - Data provided by Tarkov-Market"
        )
        await interaction.response.send_message(embed=embed) 
    except:
        embed = discord.Embed(
                    title="TarkovChangesBot - Error",
                    color=0x780A81,
                )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid item ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'ammo', description='Check the stat of an ammo via Tarkov-Changes API') #guild specific slash command
async def ammo(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        astat = EFT.check_astat(lang, data)
        name = astat.name
        newname = name.replace(" ", "%20")
        embed = discord.Embed(
            title=astat.name,
            url=f"https://tarkov-changes.com/item/{newname}",
            description=astat.description[0:240],
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(
                astat.bsgID
            )
        )
        embed.add_field(
            name=localized_string(lang, "ammoFlesh"),
            value=astat.damage,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "ammoPen"),
            value=astat.penetration,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "ammoArmor"),
            value=astat.armorDamage,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "ammoAccuracy"),
            value=astat.accuracy,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "ammoRecoil"),
            value=astat.recoil,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "ammoFrag"),
            value=astat.fragmentation,
            inline=True,
        )
        await interaction.response.send_message(embed=embed) 
    except Exception as e:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid ammo item ; please try again.",
            inline=True,
        )
        print(e)
        await interaction.response.send_message(embed=embed) 

@tree.command(name = 'armor', description='Check the stat of an armor via Tarkov-Changes API') #guild specific slash command
async def armor(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        armor = EFT.check_armor(lang, data)
        embed = discord.Embed(
            title=armor.armorName,
            url=armor.wikiLink,
            description=localized_string(lang, "armorZones") + armor.armorZones,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(
                armor.bsgID
            )
        )
        embed.add_field(
            name=localized_string(lang, "armorClass"),
            value=armor.armorClass,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "armorMaterial"),
            value=armor.armorMaterial,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "armorDurability"),
            value=armor.armorDurability,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "armorMoveSpeed"),
            value=armor.armorMoveSpeed,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "armorTurnSpeed"),
            value=armor.armorTurnSpeed,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "armorErgo"),
            value=armor.armorErgo,
            inline=True,
        )
        embed.set_footer(
            text=localized_string(lang, "armorEffectiveDurability")
            + armor.armorEffectiveDurability
            + " - Data provided by Tarkov-Changes"
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid armor item ; please try again.",
            inline=True,
        )
        print(e)
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'helmet', description='Check the stat of a helmet via Tarkov-Changes API') #guild specific slash command
async def helmet(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        helmet = EFT.check_helmets(lang, data)
        embed = discord.Embed(
            title=helmet.name,
            url=helmet.wikiLink,
            description=helmet.description,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(
                helmet.bsgID
            )
        )
        embed.add_field(
            name=localized_string(lang, "helmetZones"),
            value=helmet.armorZones,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetClass"),
            value=helmet.armorClass,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetDurability"),
            value=helmet.armorDurability,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetRicochet"),
            value=helmet.armorRico,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetMoveSpeed"),
            value=helmet.armorMoveSpeed,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetTurnSpeed"),
            value=helmet.armorTurnSpeed,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetErgo"),
            value=helmet.armorErgo,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetSoundReduc"),
            value=helmet.helmetSoundReduc,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "helmetBlocksHeadset"),
            value=helmet.helmetBlocksHeadset,
            inline=True,
        )
        await interaction.response.send_message(embed=embed)
    except:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid helmet item ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'meds', description='Check the stat of a med item via Tarkov-Changes API') #guild specific slash command
async def meds(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        medical = EFT.check_medical(lang, data)
        embed = discord.Embed(
            title=medical.name,
            url=medical.wikiLink,
            description=medical.description,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(
                medical.bsgID
            )
        )
        embed.add_field(
            name=localized_string(lang, "medUseTime"),
            value=medical.useTime,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "maxItemHP"),
            value=medical.resources,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "maxHealPerUse"),
            value=medical.resourceRate,
            inline=True,
        )

        await interaction.response.send_message(embed=embed)
    except:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid medical item ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'maps', description='Check the details of a map via Tarkov-Changes API') #guild specific slash command
async def maps(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        maps = EFT.check_maps(lang, data)
        embed = discord.Embed(
            title=maps.name,
            url=maps.wikiLink,
            description=maps.features,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(maps.shortName)
        )
        embed.add_field(
            name=localized_string(lang, "mapPlayers"),
            value=maps.players,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "mapDuration"),
            value=maps.duration,
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "mapEnemies"),
            value=maps.enemies,
            inline=True,
        )
        await interaction.response.send_message(embed=embed)
    except:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid map name ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'tax', description='Check the flea market tax of an item via Tarkov-Changes API. EX: /tax 7500000 red keycard') #guild specific slash command
async def tax(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        USAGE = localized_string(lang, "taxUsage")
        if not data:
            return USAGE
        parts = data.split()
        if len(parts) < 2:
            return localized_string(lang, "taxUsage")
        amount = safe_int(parts[0], 0)
        if amount == 0:
            return USAGE
        query = " ".join(parts[1:])
        tax_amount = EFT.check_tax(lang, amount, query)
        if not tax_amount:
            return USAGE
        (tax, model) = tax_amount
        profit = amount - tax
        embed = discord.Embed(
            title=model.name,
            url=model.wikiLink,
            color=0x780A81,
        )
        embed.set_thumbnail(url=model.img)
        embed.add_field(
            name=localized_string(lang, "taxBasePrice"),
            value=format(int(model.basePrice), ",") + " ₽",
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "taxBaseTax"),
            value=format(int(tax), ",") + " ₽",
            inline=True,
        )
        embed.add_field(
            name=localized_string(lang, "taxProfit"),
            value=format(int(profit), ",") + " ₽",
            inline=True,
        )
        embed.set_footer(
            text=localized_string(lang, "marketUpdated")
            + maya.MayaDT.from_datetime(model.updated).slang_time()
            + " - Data provided by Tarkov-Market"
        )
        await interaction.response.send_message(embed=embed)
    except:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid map name ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name = 'banned', description='Check if an item is banned from being sold on the flea-market') #guild specific slash command
async def banned(interaction: discord.Interaction, data: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        banned = EFT.check_banned(lang, data)
        embed = discord.Embed(
            title=banned.name,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(banned.bsgID)
        )
        embed.add_field(
            name=localized_string(lang, "bannedItem"),
            value=banned.banned,
            inline=True,
        )
        await interaction.response.send_message(embed=embed)
    except:
        embed = discord.Embed(
            title="TarkovChangesBot - Error",
            color=0x780A81,
        )
        embed.set_thumbnail(url="https://illogical.network/api/error.png")
        embed.add_field(
            name="Invalid Item Search",
            value="You've entered in an invalid map name ; please try again.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)


dcToken = os.environ.get("LOGIC_DISCORD_TOKEN")
client.run(dcToken)