import os
import discord
import random as rand
from random import randrange
from datetime import datetime, timedelta
from dotenv import load_dotenv

import _constants as const





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


def get_uptime_string():
	uptime = datetime.now() - start_time
	uptime_in_s = uptime.total_seconds()
	days = int(divmod(uptime_in_s, 86400)[0])
	hours = int(divmod(uptime_in_s, 3600)[0] % 24)
	minutes = int(divmod(uptime_in_s, 60)[0] % 60)
	seconds = uptime.seconds % 60

	time = ""
	if days > 0:
		time += str(days) + " day" + ("s, " if days > 1 else ", ")
	if hours > 0:
		time += str(hours) + " hour" + ("s, " if hours > 1 else ", ")
	if minutes > 0:
		time += str(minutes) + " minute" + ("s and " if minutes > 1 else " and ")
	time += str(seconds) + " second" + ("s" if seconds != 1 else "")
	return time

def get_random_line_from_file(filename):
	f = open(filename)
	l = next(f)
	for num, line in enumerate(f, 2):
		if rand.randrange(num):
			continue
		l = line
	return l.strip().replace("\\n", "\n")

def get_all_lines_from_file(filename):
	with open(filename) as f:
		return f.read().splitlines()





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

#
#
#

"""
		MAIN
	----------------------------------------------------------------------------
"""
# Run Olaf.
client.run(TOKEN)
