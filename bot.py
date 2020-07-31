import os
import settings
from twitchio.ext import commands
import json
import requests
import mysql.connector as mysql
from datetime import datetime, timedelta
import asyncio
import time

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


	def get_cd(self, name):
		self.sql.execute("SELECT cooldown FROM channels WHERE name = %s", (name,))
		cd = self.sql.fetchone()
		if cd is None:
			return cd
		else:
			return cd[0]

	#tic
	def get_lang(self, name):
		self.sql.execute("SELECT lang FROM channels WHERE name = %s", (name,))
		lang = self.sql.fetchone()
		if lang is None:
			return lang
		else:
			return lang[0]


	def get_channels(self):
		self.db.commit()
		self.sql.execute("SELECT display_name from users")
		return [i[0] for i in self.sql.fetchall()]

#Custom loop
async def check_database():
    print('Initiating loop. Waiting 30 seconds\n')
    await asyncio.sleep(30)
    print('Starting check loop\n')
    while True:
        await asyncio.sleep(16)
        print('Searching for new channels in database')

        db_channels = db.get_channels()
        unjoined_channels = []
        for i in db_channels:
            if not i in channels:
                unjoined_channels.append(i)
                channels.append(i)

        print('Joining new channels: {}\n'.format(str(unjoined_channels)))
        otp = await bot.join_channels(unjoined_channels)

def check_cooldown(name, cooldown_obj):
	cooldown = db.get_cd(name)
	if cooldown is None:
		cooldown = settings.default_cooldown
	return not datetime.utcnow() - cooldown_obj['last_usage'] > timedelta(seconds=cooldown)

#tic
def check_lang(name):
	return db.get_lang(name)



#global variables/objects
cooldowns = []
db = database()
channels = list(dict.fromkeys(db.get_channels()+settings.initial_channels))
#print("Found channels: " + str(channels))
#print(channels[:99])
loop = asyncio.get_event_loop()
asyncio.ensure_future(check_database())
#tic
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
		await ctx.channel.send('@{} - {}'.format(ctx.author.name, locale[check_lang(ctx.channel.name)]["1"]))
		#await ctx.channel.send('@{} - You must input a valid item name. EX: Slick'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.price_link+'{}'.format(req)).text
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
		await ctx.channel.send('@{} - You must input a valid item name. EX: Slick'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.slot_link+'{}'.format(req)).text
	await ctx.channel.send('@{} {}'.format(ctx.author.name, response))

@bot.command(name="trader")
async def trader(ctx, *req):
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
		await ctx.channel.send('@{} - You must input a valid item name. EX: Slick'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.trader_link+'{}'.format(req)).text
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
		await ctx.channel.send('@{} - You must input a valid item name. EX: Slick'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.wiki_link+'{}'.format(req)).text
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
		await ctx.channel.send('@{} - You must input a valid ammo name. EX: 9x19mm PST Gzh'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.ammo_link+'{}'.format(req)).text
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
		await ctx.channel.send('@{} - You must input a valid medical item name.'.format(ctx.author.name))
		return

	#Check if cooldown object for channel is in cooldowns list and update last usage
	if cd is None:
		cooldowns.append({'name': ctx.channel.name, 'last_usage': datetime.utcnow()})
	else:
		cd_obj['last_usage'] = datetime.utcnow()
	
	req = ' '.join(req)
	print('Searching for %s\n' % req)
	response = requests.get(url=settings.medical_link+'{}'.format(req)).text
	await ctx.channel.send('@{} {}'.format(ctx.author.name, response))


@bot.command(name="eftbot")
async def eftbot(ctx, req=None):
	await ctx.channel.send("@" + ctx.author.name + " - Commands available: !astat , !price , !medical , !slot , !trader , and !wiki ~ More commands coming soon!")
	return

@bot.command(name="help")
async def help(ctx, req=None):
	await ctx.channel.send("@" + ctx.author.name + " - Commands available: !astat  , !price , !medical , !slot , !trader , and !wiki ~ More commands coming soon!")
	return


@bot.command(name="addbot")
async def addbot(ctx, req=None): #Later change this to invite link
	await ctx.channel.send("@" + ctx.author.name + " - If you want the bot in your channel, head to https://illogical.network/ and click 'EFT Bot' to add the bot!.")
	return

@bot.command(name="setCD")
async def setCD(ctx, cd=settings.default_cooldown):
	if not ctx.author.is_mod:
		return
	
	db.update_cooldown(ctx.channel.name, cd)		
	await ctx.channel.send('Cooldown has been set to {}'.format(cd))



@bot.event
async def event_command_error(ctx, err):
	if type(err) != commands.errors.BadArgument:
		pass
	else:
		print('Command was given a bad argument, ignoring errors')



if __name__ == "__main__":
	bot.run()
