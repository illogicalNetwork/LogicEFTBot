import os
import settings
from twitchio.ext import commands
import json
import requests
import mysql.connector as mysql
from datetime import datetime, timedelta
import asyncio
import time
import logging

#db config
class database:
    def __init__(self):
        db = mysql.connect(
            host = settings.database_config["host"],
            user = settings.database_config["user"],
            passwd = settings.database_config["passwd"],
            database = settings.database_config["database"]
        )

        sql = db.cursor(buffered=True)
        db.commit()
        self.db = db
        self.sql = sql

    def update_cooldown(self, name, cooldown):
        self.sql.execute("REPLACE INTO channels (name, cooldown) VALUES (%s, %s)", (name, cooldown))
        self.db.commit()

    def update_lang(self, name, lang, uname):
        #self.sql.execute("UPDATE users SELECT username, lang VALUES (%s, %s)", (name, lang))
        self.sql.execute("UPDATE users SET username=%s, lang=%s WHERE username=%s", (name,lang, uname))
        self.db.commit()

    def get_cd(self, name):
        self.sql.execute("SELECT cooldown FROM channels WHERE name = %s", (name,))
        cd = self.sql.fetchone()
        if cd is None:
            return cd
        else:
            return cd[0]

    def get_lang(self, name):
        self.sql.execute("SELECT lang FROM users WHERE username = %s", (name,))
        lang = self.sql.fetchone()
        if lang is None:
            return lang
        else:
            return lang[0]

    def get_channels(self):
        self.db.commit()
        self.sql.execute("SELECT username from users")
        return [i[0] for i in self.sql.fetchall()]

#Custom loop
async def check_database():
    print('Initiating loop. Waiting 15 seconds\n')
    await asyncio.sleep(15)
    print('Starting check loop\n')
    while True:
        await asyncio.sleep(10)
        #print('Searching for new channels in database')

        db_channels = db.get_channels()
        unjoined_channels = []
        for i in db_channels:
            if not i in channels:
                unjoined_channels.append(i)
                channels.append(i)

        #print('Joining new channels: {}\n'.format(str(unjoined_channels)))
        otp = await bot.join_channels(unjoined_channels)

def check_cooldown(name, cooldown_obj):
    cooldown = db.get_cd(name)
    if cooldown is None:
        cooldown = settings.default_cooldown
    return not datetime.utcnow() - cooldown_obj['last_usage'] > timedelta(seconds=cooldown)

def check_lang(name):
    return db.get_lang(name)

#global variables/objects
cooldowns = []
db = database()
channels = list(dict.fromkeys(db.get_channels()+settings.initial_channels))
loop = asyncio.get_event_loop()
asyncio.ensure_future(check_database())
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('test.log', 'a'))
print = logger.info

locale = []
with open("localizations.json", "r") as read_file:
    locale = json.load(read_file)


bot = commands.Bot(
    loop=loop,
    irc_token=settings.irc_token,
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    nick=settings.nick,
    prefix=settings.prefix,
    initial_channels=channels[:99]
)

@bot.event
async def event_ready():
    print("I am online!\n")
    ws = bot._ws
    if len(channels) > 100:
        pack = 1
        while len(channels) > pack * 100:
                time.sleep(16)
                pack += 1
                print(f'Joining pack #{pack}\n')
                await bot.join_channels(channels[pack*100-101:pack*100-1])
    
@bot.command(name="price")
async def price(ctx, *req):
    #Look for cooldown object in cooldowns global variable
    cd = None
    for i in cooldowns:
        if i['name'] == ctx.channel.name:
            cd = check_cooldown(ctx.channel.name, i) #Check if cooldown is over
            cd_obj = i
            break

    if cd or ctx.author.name.lower() == settings.nick:
        return

    if len(req) == 0:
        #tic
        await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["validItem"]))
        return

    #Check if cooldown object for channel is in cooldowns list and update last usage
    if cd is None:
        cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
    else:
        cd_obj['last_usage'] = datetime.utcnow()
    
    req = ' '.join(req)
    print(ctx.channel.name + ' - searching for %s\n' % req)
    ###NEW
    lang = check_lang(ctx.channel.name)
    price_link = None
    if lang == "en":
        price_link = settings.price_link_en
    elif lang == "de":
        price_link = settings.price_link_de
    elif lang == "es":
        price_link = settings.price_link_es
    elif lang == "tr":
        price_link = settings.price_link_tr
    elif lang == "nl":
        price_link = settings.price_link_nl
    crafted_url = price_link + "{}".format(req)
    response = requests.get(url = crafted_url).text
    ###NEW
    await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="slot")
async def slot(ctx, *req):
    #Look for cooldown object in cooldowns global variable
    cd = None
    for i in cooldowns:
        if i['name'] == ctx.channel.name:
            cd = check_cooldown(ctx.channel.name, i) #Check if cooldown is over
            cd_obj = i
            break

    if cd or ctx.author.name.lower() == settings.nick:
        return

    if len(req) == 0:
        await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["validItem"]))
        return

    #Check if cooldown object for channel is in cooldowns list and update last usage
    if cd is None:
        cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
    else:
        cd_obj['last_usage'] = datetime.utcnow()
    
    req = ' '.join(req)
    print(ctx.channel.name + ' - searching for %s\n' % req)
    lang = check_lang(ctx.channel.name)
    slot_link = None
    if lang == "en":
        slot_link = settings.slot_link_en
    elif lang == "de":
        slot_link = settings.slot_link_de
    elif lang == "es":
        slot_link = settings.slot_link_es
    elif lang == "tr":
        slot_link = settings.slot_link_tr
    elif lang == "nl":
        slot_link = settings.slot_link_nl 
    crafted_url = slot_link + "{}".format(req)
    response = requests.get(url = crafted_url).text
    await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="wiki")
async def wiki(ctx, *req):
    #Look for cooldown object in cooldowns global variable
    cd = None
    for i in cooldowns:
        if i['name'] == ctx.channel.name:
            cd = check_cooldown(ctx.channel.name, i) #Check if cooldown is over
            cd_obj = i
            break

    if cd or ctx.author.name.lower() == settings.nick:
        return

    if len(req) == 0:
        await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["validItem"]))
        return

    #Check if cooldown object for channel is in cooldowns list and update last usage
    if cd is None:
        cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
    else:
        cd_obj['last_usage'] = datetime.utcnow()
    
    req = ' '.join(req)
    print(ctx.channel.name + ' - searching for %s\n' % req)
    lang = check_lang(ctx.channel.name)
    wiki_link = None
    if lang == "en":
        wiki_link = settings.wiki_link_en
    elif lang == "de":
        wiki_link = settings.wiki_link_de
    elif lang == "es":
        wiki_link = settings.wiki_link_es
    elif lang == "tr":
        wiki_link = settings.wiki_link_tr
    elif lang == "nl":
        wiki_link = settings.wiki_link_nl
    crafted_url = wiki_link + "{}".format(req)
    response = requests.get(url = crafted_url).text
    await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="astat")
async def astat(ctx, *req):
    #Look for cooldown object in cooldowns global variable
    cd = None
    for i in cooldowns:
        if i['name'] == ctx.channel.name:
            cd = check_cooldown(ctx.channel.name, i) #Check if cooldown is over
            cd_obj = i
            break

    if cd or ctx.author.name.lower() == settings.nick:
        return

    if len(req) == 0:
        await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["validAmmo"]))
        return

    #Check if cooldown object for channel is in cooldowns list and update last usage
    if cd is None:
        cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
    else:
        cd_obj['last_usage'] = datetime.utcnow()
    
    req = ' '.join(req)
    print(ctx.channel.name + ' - searching for %s\n' % req)
    lang = check_lang(ctx.channel.name)
    ammo_link = None
    if lang == "en":
        ammo_link = settings.ammo_link_en
    elif lang == "de":
        ammo_link = settings.ammo_link_de
    elif lang == "es":
        ammo_link = settings.ammo_link_es
    elif lang == "tr":
        ammo_link = settings.ammo_link_tr
    elif lang == "nl":
        ammo_link = settings.ammo_link_nl  
    crafted_url = ammo_link + "{}".format(req)
    response = requests.get(url = crafted_url).text
    await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="medical")
async def medical(ctx, *req):
    #Look for cooldown object in cooldowns global variable
    cd = None
    for i in cooldowns:
        if i['name'] == ctx.channel.name:
            cd = check_cooldown(ctx.channel.name, i) #Check if cooldown is over
            cd_obj = i
            break

    if cd or ctx.author.name.lower() == settings.nick:
        return

    if len(req) == 0:
        await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["validMed"]))
        return

    #Check if cooldown object for channel is in cooldowns list and update last usage
    if cd is None:
        cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
    else:
        cd_obj['last_usage'] = datetime.utcnow()
    
    req = ' '.join(req)
    print(ctx.channel.name + ' - searching for %s\n' % req)
    lang = check_lang(ctx.channel.name)
    medical_link = None
    if lang == "en":
        medical_link = settings.medical_link_en
    elif lang == "de":
        medical_link = settings.medical_link_de
    elif lang == "es":
        medical_link = settings.medical_link_es
    elif lang == "tr":
        medical_link = settings.medical_link_tr
    elif lang == "nl":
        medical_link = settings.medical_link_nl  
    crafted_url = medical_link + "{}".format(req)
    response = requests.get(url = crafted_url).text
    await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="eftbot")
async def eftbot(ctx, req=None):
    await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["botHelp"]))
    return

@bot.command(name="help")
async def help(ctx, req=None):
    await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["botHelp"]))
    return

@bot.command(name="addbot")
async def addbot(ctx, req=None): #Later change this to invite link
    await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["addBot"]))
    return

@bot.command(name="setCD")
async def setCD(ctx, cd=settings.default_cooldown):
    if not ctx.author.is_mod:
        await ctx.channel.send("@" + ctx.author.name + " You ain't a mod you dingus!")
        return
    db.update_cooldown(ctx.channel.name, cd)        
    await ctx.channel.send("@" + ctx.author.name + ' - Cooldown has been set to {}'.format(cd))

@bot.command(name="setLang")
async def setLang(ctx, lang=settings.default_lang):
    if not ctx.author.is_mod:
        await ctx.channel.send("@" + ctx.author.name + " You ain't a mod you dingus!")
        return
    db.update_lang(ctx.channel.name, lang, ctx.channel.name)        
    await ctx.channel.send("@" + ctx.author.name + ' - Language has been set to {}'.format(lang))   

@bot.event
async def event_command_error(ctx, err):
    if type(err) != commands.errors.BadArgument:
        pass
    else:
        print('Command was given a bad argument, ignoring errors')

if __name__ == "__main__":
    bot.run()
