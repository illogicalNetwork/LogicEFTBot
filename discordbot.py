import discord
from discord import app_commands
from discord.ext import tasks
from bot.config import settings, localized_string
from bot.database import Database
from bot.eft import EFT
from bot.log import log
from bot.models import (
    safe_int,
)
import maya
import os
import time
import requests
import asyncio
from datetime import datetime, timedelta

tarkov_ratio = 7

CHANNEL_ID = 1086442564686721085

def hrs(num):
    return 1000 * 60 * 60 * num

def real_time_to_tarkov_time(time, left):
    one_day = hrs(24)
    russia = hrs(3)
    offset = russia + (0 if left else hrs(12))
    tarkov_time = datetime.utcfromtimestamp(((offset + time.timestamp() * 1000 * tarkov_ratio) % one_day) / 1000)
    return tarkov_time

def format_hms(date):
    return f'{date.hour:02d}:{date.minute:02d}:{date.second:02d}'

def get_tarkov_time(minutes):
    now = datetime.utcnow()
    time_to_add = timedelta(minutes=minutes)
    left_time = real_time_to_tarkov_time(now + time_to_add, True)
    right_time = real_time_to_tarkov_time(now + time_to_add, False)
    return {
        'left': format_hms(left_time),
        'right': format_hms(right_time)
    }

def get_trader_resets():
    url = 'http://api.tarkov-changes.com/v1/traderResets'
    headers = {'AUTH-TOKEN': 'redacted'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []

def create_trader_embed(trader_name, next_resupply):
    embed = discord.Embed(
        title=f"{trader_name} resupply incoming!",
        description=f"{trader_name} resupply - <t:{int(next_resupply)}:R>.",
    )
    base_url = "https://tarkov-changes.com/img/traders/"
    if trader_name == "Prapor":
        embed.color = discord.Color.purple()
        embed.set_thumbnail(url=f"{base_url}/prapor-portrait.png")
        content = "<@&1086442704201859142>"
    elif trader_name == "Therapist":
        embed.color = discord.Color.purple()
        content = "<@&1086442647570350270>"
        embed.set_thumbnail(url=f"{base_url}/therapist-portrait.png")
    elif trader_name == "Skier":
        embed.color = discord.Color.purple()
        content = "<@&1086442718370205867>"
        embed.set_thumbnail(url=f"{base_url}/skier-portrait.png")
    elif trader_name == "Peacekeeper":
        embed.color = discord.Color.purple()
        content = "<@&1086442736531542066>"
        embed.set_thumbnail(url=f"{base_url}/peacekeeper-portrait.png")
    elif trader_name == "Mechanic":
        embed.color = discord.Color.purple()
        content = "<@&1086442774334820423>"
        embed.set_thumbnail(url=f"{base_url}/mechanic-portrait.png")
    elif trader_name == "Ragman":
        embed.color = discord.Color.purple()
        content = "<@&1086442756911665233>"
        embed.set_thumbnail(url=f"{base_url}/ragman-portrait.png")
    elif trader_name == "Jaeger":
        embed.color = discord.Color.purple()
        content = "<@&1086442804600905861>"
        embed.set_thumbnail(url=f"{base_url}/jeager-portrait.png")
    else: 
        pass
    return embed, content

async def delete_message_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

class LogicEFTClient(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = (
            False  # we use this so the bot doesn't sync commands more than once
        )

    @tasks.loop(seconds=60)
    async def check_resupply(self):
        channel = self.get_channel(CHANNEL_ID)
        trader_resets = get_trader_resets()
        current_time = time.time()

        # Initialize the last_posted_times dictionary if it doesn't exist
        if not hasattr(self, 'last_posted_times'):
            self.last_posted_times = {}

        for trader in trader_resets:
            trader_id = trader['_id']
            time_remaining = trader['nextResupply'] - current_time

            # Check if we've posted about this trader before
            last_posted_time = self.last_posted_times.get(trader_id, 0)
            time_since_last_post = current_time - last_posted_time

            if 0 <= time_remaining <= 300 and time_since_last_post > 300:  # Within 5 minutes and at least 5 minutes since the last post
                if trader_id == "Fence":
                    print("Fence - Passed")
                elif trader_id == "Lightkeeper":
                    print("Lightkeeper - Passed")
                else:
                    embed, content = create_trader_embed(trader_id, trader['nextResupply'])
                    sent_message = await channel.send(content=content, embed=embed)
                    self.last_posted_times[trader_id] = current_time  # Update the last posted time for this trader
                    # Call the delete_message_after_delay function
                    asyncio.create_task(delete_message_after_delay(sent_message, 600))

    async def on_ready(self):
        stream = discord.Streaming(
            platform="Twitch",
            name="/price & /tax » https://eft.bot",
            url="https://twitch.tv/TarkovChangesBot",
        )
        await client.change_presence(activity=stream)
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")
        client.check_resupply.start()

client = LogicEFTClient()
tree = app_commands.CommandTree(client)
db = Database()

@tree.command(description="Check the price of an item via Tarkov-Market API")
@app_commands.describe(item="Please enter in an item name.")
async def price(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        price = EFT.check_price(lang, item)
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


@tree.command(description="Check the stat of an ammo via Tarkov-Changes API")  
@app_commands.describe(ammo="Please enter in an ammo name.")
async def ammo(interaction: discord.Interaction, ammo: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        astat = EFT.check_astat(lang, ammo)
        name = astat.name
        newname = name.replace(" ", "%20")
        embed = discord.Embed(
            title=astat.name,
            url=f"https://tarkov-changes.com/item/{newname}",
            description=astat.description[0:240],
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(astat.bsgID)
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


@tree.command(description="Check the stat of an armor via Tarkov-Changes API")  
@app_commands.describe(item="Please enter in an armor name.")
async def armor(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        armor = EFT.check_armor(lang, item)
        embed = discord.Embed(
            title=armor.armorName,
            url=armor.wikiLink,
            description=localized_string(lang, "armorZones") + armor.armorZones,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(armor.bsgID)
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


@tree.command(description="Check the stat of a helmet via Tarkov-Changes API") 
@app_commands.describe(item="Please enter in a helmet name.")
async def helmet(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        helmet = EFT.check_helmets(lang, item)
        embed = discord.Embed(
            title=helmet.name,
            url=helmet.wikiLink,
            description=helmet.description,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(helmet.bsgID)
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


@tree.command(description="Check the stat of a med item via Tarkov-Changes API")
@app_commands.describe(item="Please enter in an medical item name.")
async def meds(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        medical = EFT.check_medical(lang, item)
        embed = discord.Embed(
            title=medical.name,
            url=medical.wikiLink,
            description=medical.description,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/items/128/{0}.png".format(medical.bsgID)
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


@tree.command(description="Check the details of a map via Tarkov-Changes API")
@app_commands.describe(map="Please enter in a valid map name.")
async def maps(interaction: discord.Interaction, map: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        maps = EFT.check_maps(lang, map)
        embed = discord.Embed(
            title=maps.name,
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://tarkov-changes.com/img/maps/{0}.png".format(maps.name).lower()
        )
        embed.add_field(
            name="Player Count",
            value=f"`{maps.minCount} - {maps.maxCount}`",
            inline=False,
        )
        embed.add_field(
            name="Raid Duration",
            value=f"`{maps.duration}`",
            inline=False,
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
            value="You've entered in an invalid map name ; please try again.",
            inline=True,
        )
        print(e)
        await interaction.response.send_message(embed=embed)


@tree.command(description="Check the flea market tax of an item via Tarkov-Changes API. EX: /tax 7500000 red keycard",)
@app_commands.describe(item="Usage: <amount> <item>")
async def tax(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        USAGE = localized_string(lang, "taxUsage")
        if not item:
            return USAGE
        parts = item.split()
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


@tree.command(description="Check if an item is banned from being sold on the flea-market")  
@app_commands.describe(item="Please enter in an item name.")
async def banned(interaction: discord.Interaction, item: str):
    lang = db.get_lang(interaction.guild_id)
    try:
        banned = EFT.check_banned(lang, item)
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
    except Exception as e:
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
        print(str(e))

@tree.command(description="Check the time of current Tarkov Raids. Optional: See future raid time.")
@app_commands.describe(usertime="Enter time in minutes. Displays future raid time.")
async def tarkovtime(interaction: discord.Interaction, usertime:int=None):
    if usertime is None:
        lang = db.get_lang(interaction.guild_id)
        try:
            tarkovTime = EFT.tarkovTime(lang, "")
            embed = discord.Embed(
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://i.imgur.com/k3yvPND.png"
            )
            embed.add_field(
                name="Tarkov Time - Left Side",
                value=tarkovTime.left,
                inline=False,
            )
            embed.add_field(
                name="Tarkov Time - Right Side",
                value=tarkovTime.right,
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
        except:
            embed = discord.Embed(
                title="TarkovChangesBot - Error",
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            await interaction.response.send_message(embed=embed)
    if usertime:
        try:
            fTime = get_tarkov_time(usertime)
            embed = discord.Embed(
                title="Future Raid Time",
                color=0x780A81,
            )
            embed.set_thumbnail(
                url="https://i.imgur.com/k3yvPND.png"
            )
            embed.add_field(
                name="Future Tarkov Time - Left",
                value=fTime['left'],
                inline=False,
            )
            embed.add_field(
                name="Future Tarkov Time - Right",
                value=fTime['right'],
                inline=True,
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="TarkovChangesBot - Error",
                description=str(e),
                color=0x780A81,
            )
            embed.set_thumbnail(url="https://illogical.network/api/error.png")
            await interaction.response.send_message(embed=embed)

@tree.command(
    name="status", description="Check data from the Tarkov-Changes datamine tool"
)  
async def tarvkoStatus(interaction: discord.Interaction):
    lang = db.get_lang(interaction.guild_id)
    try:
        status = EFT.check_status(lang, "")
        embed = discord.Embed(
            title="Data Mine - Status Check",
            description="This data is aggregated around every 10-15 minutes. The average level is compiled based off the users \"Looking for group\" in all lobbies.",
            color=0x780A81,
        )
        embed.set_thumbnail(
            url="https://i.imgur.com/sDW5405.png"
        )
        embed.add_field(
            name="EFT Game Version",
            value=status.eft_version,
            inline=True,
        )
        embed.add_field(
            name="Lobby Average LVL",
            value=status.lobby_average,
            inline=True,
        )
        embed.add_field(
            name="",
            value="",
            inline=False,
        )
        embed.add_field(
            name="Highest Level Player",
            value=f"`{status.highest_level_name}`",
            inline=True,
        )
        embed.add_field(
            name="Highest Level & Region",
            value=f"`{status.highest_level}` | `{status.highest_level_region}`",
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

client.run("redacted")
