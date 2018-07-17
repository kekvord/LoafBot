import discord
import asyncio
import sqlite3
import datetime
from discord.ext import commands

con = sqlite3.connect('discord.db')
con.row_factory = sqlite3.Row

def __init__(self, bot):
	self.bot = bot

async def send_modlogs(bot, guild, *args, **kwargs):
	c = con.cursor()
	c.execute("SELECT * FROM guilds WHERE guildid=?", (guild.id,))
	row = c.fetchone()
	if row['modlogs'] is not None:
		await bot.get_channel(row['modlogs']).send(*args, **kwargs)

async def send_publiclogs(bot, guild, *args, **kwargs):
	c = con.cursor()
	c.execute("SELECT * FROM guilds WHERE guildid=?", (guild.id,))
	row = c.fetchone()
	if row['modlogs'] is not None:
		await bot.get_channel(row['modlogs']).send(*args, **kwargs)
	if row['publiclogs'] is not None:
		await bot.get_channel(row['publiclogs']).send(*args, **kwargs)

async def send_starboard(bot, guild, *args, **kwargs):
	c = con.cursor()
	c.execute("SELECT * FROM guilds WHERE guildid=?", (guild.id,))
	row = c.fetchone()
	if row['starboard'] is not None:
		await bot.get_channel(row['starboard']).send(*args, **kwargs)

def timedelta_str(dt):
	days = dt.days
	hours, r = divmod(dt.seconds, 3600)
	minutes, sec = divmod(r, 60)
	days1, hours1, minutes1, secs1 = [(('' if x == 0 else f'{x} {y}') + ('s' if x > 1 else '')) for x,y in [(days, "day"), (hours, "hour"),  (minutes, "minute"), (sec, 'second')]]

	uptime = f"{days1} {hours1} {minutes1} {secs1}"

	return uptime

def load_prefixes(bot):
	c = con.cursor()
	for row in c.execute("SELECT * FROM prefixes WHERE guildid"):
		bot.prefixes[row['guildid']] = row['prefix']

def get_pre(bot, message):
	if message.content.startswith('>'):
		return '>'
	else:
		try:
			return bot.prefixes[message.guild.id]
		except:
			return '>'

def update_time(bot, guild, memberid):
	c = con.cursor()
	time = datetime.datetime.now()
	try:
		try:
			c.execute('UPDATE times SET time=(?) WHERE id=(?) AND guildid=(?)', (time, memberid, guild.id))
		except:
			c.execute('INSERT INTO times VALUES (?, ?, ?)', (guild.id, memberid, time))
	except:
		c.execute('''CREATE TABLE times
			     (guildid integer, id integer, time datetime)''')
		c.execute('INSERT INTO guilds VALUES (?, ?, ?)', (guild.id, memberid, time))
	con.commit()

def prune_members(bot, ctx, weeks):
	time = datetime.datetime.now()
	c = con.cursor()
	pruned = []
	for member in ctx.guild.members:
		c.execute("SELECT * FROM times WHERE id=? AND guildid=?", (member.id, ctx.guild.id))
		row = c.fetchone()
		if datetime.strptime(row['time'], '%m/%d/%Y %I:%M:%S %p') + datetime.timedelta(weeks=weeks) >= time:
			pass
		else:
			c.execute("DELETE * FROM times WHERE id=? AND guildid=?", (member.id, ctx.guild.id))
			pruned.append(member)
		return pruned

def get_muterole(guild):
	c = con.cursor()
	c.execute("SELECT * FROM guilds WHERE guildid=?", (guild.id,))
	row = c.fetchone()
	return discord.utils.get(guild.roles, id=row['muterole'])

def get_field(guild, field):
	c = con.cursor()
	c.execute("SELECT * FROM guilds WHERE guildid=?", (guild.id,))
	row = c.fetchone()
	return row[field]

def set_embed_image_to_message_image(em, message):
	try:
		if message.content.startswith('https://'):
			em.set_image(url=message.content)
	except:
		pass
	try:
		attach = message.attachments
		em.set_image(url = attach[0].url)
	except:
		pass
