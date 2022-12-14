import os
import discord
import random as rand
import threading
import asyncio
from random import randrange
from datetime import datetime, timedelta
from dotenv import load_dotenv
from discord.ext import tasks, commands

import _constants as const





"""
		CLASSES
	----------------------------------------------------------------------------
"""
class TimerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.f_loop.start()

	def cog_unload(self):
		self.f_loop.cancel()

	@tasks.loop(seconds = 1.0)	# Call check_timers() every second.
	async def f_loop(self):
		await check_timers()

class OlafTimer:
	def __init__(self, user_id, channel, hours, minutes, seconds, text):
		global olaf_timer_id
		self.id = olaf_timer_id
		olaf_timer_id += 1

		self.user_id = user_id
		self.channel = channel
		self.text = text

		self.start = datetime.now()
		self.end = self.start + timedelta(\
			hours = hours if hours != -1 else 0, \
			minutes = minutes if minutes != -1 else 0, \
			seconds = seconds \
		)

	def get_user_id(self):
		return self.user_id

	def get_text(self):
		return self.text

	def get_channel(self):
		return self.channel

	def is_expired(self):
		return self.end - self.start < 0





"""
		INITIAL SETUP
	----------------------------------------------------------------------------
"""
# Load the temporary environment variables.
load_dotenv()
# The bot's secret token.
TOKEN = os.getenv("DISCORD_TOKEN")





"""
		GLOBAL VARIABLES
	----------------------------------------------------------------------------
"""
# Timestamp of initial connection establishment.
start_time = None

# The discord client instance and its required args.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# The starting ID of Discord timers.
olaf_timer_id = 1
# The array holding all currently active timers.
olaf_timer_dict = {}





"""
		FUNCTIONS
	----------------------------------------------------------------------------
"""
# Called when Olaf successfully connected to Discord.
@client.event
async def on_ready():
	# Set current time as boot time.
	global start_time
	start_time = datetime.now()
	# Print connection success message to console.
	print(f"{client.user} has connected to Discord!")


# Called when a new message arrives.
@client.event
async def on_message(msg):
	# If message comes from bot, ignore it.
	if msg.author == client.user:
		return

	# Get message contents.
	m = msg.content

	# Analyse the message.
	if m.startswith("!") and m != "!":	# Is message a command?
		# Remove the '!' from the message.
		m = m[1:]
		# Array containing all parts of the command.
		m_parts = m.split()

		match m_parts[0]:
			case "help":
				await help(msg.channel)
			case "ping":
				await ping(msg.channel)
			case "info":
				await send_info(msg.channel)
			case "uptime":
				await uptime(msg.channel)
			case "timer":
				match len(m_parts):
					case 2:
						add_timer(msg.author.id, msg.channel, m_parts[1], None)
					case 3:
						add_timer(msg.author.id, msg.channel, m_parts[1], m_parts[2])
					case _:
						await msg.channel.send("Wrong syntax buddy: `!timer [hh:mm:ss|mm:ss|ss] (text)`")
			case "quote":
				await quote(msg.channel)
			case "insult":
				await insult(msg.channel)
			case "fun" | "fact" | "funfact":
				await fun_fact(msg.channel)

			case _:
				await invalid_command_response(msg.channel)
	else:
		# Check if the message is an emoji.
		match m:
			case ":D":
				if randrange(2) == 0:
					await msg.channel.send(":D")
			case ":3":
				if randrange(2) == 0:
					await msg.channel.send(":3")
			case ":o":
				if randrange(2) == 0:
					await msg.channel.send(":o")
			case ":(":
				if randrange(2) == 0:
					await msg.channel.send(":(")
			case "<:kekw:832295185354457089>":
				if randrange(2) == 0:
					await msg.channel.send("<:kekw:832295185354457089>")
			case "<:omegalul:1019944484609458207>":
				if randrange(2) == 0:
					await msg.channel.send("<:omegalul:1019944484609458207>")


# Returns a string containing how long Olaf's been online for.
def get_uptime_string():
	uptime = datetime.now() - start_time
	uptime_in_s = uptime.total_seconds()
	days = int(divmod(uptime_in_s, 86400)[0])
	hours = int(divmod(uptime_in_s, 3600)[0] % 24)
	minutes = int(divmod(uptime_in_s, 60)[0] % 60)
	seconds = uptime.seconds % 60
	return prettify_time(days, hours, minutes, seconds)

# Formats hours, minutes and seconds to a pretty string.
def prettify_time(days, hours, minutes, seconds):
	time = ""
	if days > 0:
		time += str(days) + " day" + ("s, " if days > 1 else ", ")
	if hours > 0:
		time += str(hours) + " hour" + ("s, " if hours > 1 else ", ")
	if minutes > 0:
		time += str(minutes) + " minute" + ("s and " if minutes > 1 else " and ")
	time += str(seconds) + " second" + ("s" if seconds != 1 else "")
	return time

# Choose a random line from the given file and return it as a string.
def get_random_line_from_file(filename):
	f = open(filename)
	l = next(f)
	for num, line in enumerate(f, 2):
		if rand.randrange(num):
			continue
		l = line
	return l.strip().replace("\\n", "\n")

# Return the contents of the file as a list of strings.
def get_all_lines_from_file(filename):
	with open(filename) as f:
		return f.read().splitlines()



# Create a new Discord timer.
async def add_timer(user_id, channel, timestamp, text):
	t_parts = timestamp.split(":")
	h, m, s = 0, 0, 0
	match len(t_parts):
		case 1:
			s = int(t_parts[0])
		case 2:
			m, s = int(t_parts[0]), int(t_parts[1])
		case 3:
			h, m, s = int(t_parts[0]), int(t_parts[1]), int(t_parts[2])
		case _:
			await channel.send("Wrong syntax buddy! Timer duration must have 3")
	olaf_timer_dict[olaf_timer_id] = OlafTimer(user_id, channel, h, m, s, text)
	await channel.send("Timer set for " + prettify_time(0, h, m, s) + ".")
	print(len(olaf_timer_dict))

# Go through the map of Discord timers and check which timers expired.
async def check_timers():
	print("checked timers.")
	for key, value in olaf_timer_dict.items():
		if value.is_expired():	# Check if timer expired.
			t = value.get_text() if value.get_text() != None else "<no description>"
			text = "RRRRRING DING DING!!! <@" + value.get_user_id() + ">, you timer's up:\n" + t
			await value.get_channel.send(text)
			del olaf_timer_dict[key]	# Remove it from the map.
	print(len(olaf_timer_dict))





"""
		COMMANDS
	----------------------------------------------------------------------------
"""
async def help(channel):
	lines = get_all_lines_from_file("f_help.txt")
	s = ""
	for line in lines:
		s += line + "\n"
	await channel.send(s)

async def ping(channel):
	await channel.send(get_random_line_from_file("f_ping.txt"))

async def send_info(channel):
	response = "```\n"
	response += "Bot Name:       " + const.BOT_NAME + "\n"
	response += "App Version:    " + const.APP_VERSION + "\n"
	response += "Discord API:    " + const.DISCORD_API + "\n"
	response += "Coding Lang.:   " + const.CODE_LANG + "\n"
	response += "Lang. Locale:   " + const.LANG_LOCALE + "\n"
	response += "```"
	await channel.send(response)

async def uptime(channel):
	await channel.send(get_uptime_string())

async def quote(channel):
	await channel.send(get_random_line_from_file("f_quotes.txt"))

async def insult(channel):
	await channel.send(get_random_line_from_file("f_insults.txt"))

async def fun_fact(channel):
	await channel.send(get_random_line_from_file("f_funfacts.txt"))



async def invalid_command_response(channel):
	await channel.send(get_random_line_from_file("f_invalid_command.txt"))





"""
		MAIN
	----------------------------------------------------------------------------
"""
# Add check_timers() functions to main event loop of discord.py
#client.loop.create_task(check_timers())
# Run Olaf.
client.run(TOKEN)
