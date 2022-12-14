import os
from dotenv import load_dotenv
import discord
import random as rand
from discord.ext import commands, tasks
from random import randrange
from datetime import datetime, timedelta

import _constants as const





"""
		INITIAL SETUP & STATIC VARIABLES
	----------------------------------------------------------------------------
"""
# Load the temporary environment variables.
load_dotenv()

# The bot's secret token.
TOKEN = os.getenv("DISCORD_TOKEN")
# The prefix character for commands.
COMMAND_PREFIX = "!"





"""
		CLASSES
	----------------------------------------------------------------------------
"""
class OlafTimer:
	def __init__(self, user_id, channel, hours, minutes, seconds, name):
		self.user_id = user_id
		self.channel = channel
		self.name = name

		self.start = datetime.now()
		self.end = self.start + timedelta(\
			hours = hours if hours != -1 else 0, \
			minutes = minutes if minutes != -1 else 0, \
			seconds = seconds \
		)

	def get_user_id(self):
		return self.user_id

	def get_name(self):
		return self.name

	def get_channel(self):
		return self.channel

	def get_remaining(self):
		return self.end - datetime.now()

	def is_expired(self):
		return self.end < datetime.now()

	def to_string(self):
		return "Timer \"" + self.name + "\" by " + bot.get_user(self.user_id).name + \
			" expires in " + prettify_timedelta(self.get_remaining())





"""
		GLOBAL VARIABLES
	----------------------------------------------------------------------------
"""
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix = COMMAND_PREFIX, intents = intents)

# Timestamp of initial connection establishment.
start_time = None
# The starting ID of Discord timers.
#olaf_timer_id = 1
# The array holding all currently active timers.
olaf_timer_dict = dict()





"""
		FUNCTIONS
	----------------------------------------------------------------------------
"""
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

def prettify_timedelta(delta):
	s = delta.total_seconds()
	days = int(divmod(s, 86400)[0])
	hours = int(divmod(s, 3600)[0] % 24)
	minutes = int(divmod(s, 60)[0] % 60)
	seconds = delta.seconds % 60
	return prettify_time(days, hours, minutes, seconds)

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

# Go through the map of Discord timers and check which timers expired.
@tasks.loop(seconds = 1) # runs every second
async def check_timers():
	# Copy timmer dictionary temporarily.
	timer_dict = olaf_timer_dict.copy()

	for key, timer in timer_dict.items():
		if timer.is_expired():	# Check if timer expired.
			t = timer.get_name() if timer.get_name() != None else "<no description>"
			text = "RRRRRING DING DING!!! <@" + str(timer.get_user_id()) + ">, you timer's up:\n" + t
			await timer.get_channel().send(text)
			del olaf_timer_dict[key]	# Remove it from the map.
	#print(len(olaf_timer_dict))





"""
		COMMANDS & OTHER EVENTS
	----------------------------------------------------------------------------
"""
# Called when Olaf successfully connected to Discord.
@bot.event
async def on_ready():
	# Set current time as boot time.
	global start_time
	start_time = datetime.now()

	#  Start the timer check routine.
	check_timers.start()

	# Print connection success message to console.
	print(f"{bot.user} has connected to Discord!")

# Called when a new message arrives.
@bot.event
async def on_message(msg):
	# If message comes from bot, ignore it.
	if msg.author == bot.user:
		return

	# Get message contents.
	m = msg.content

	# Analyse the message.
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
		case "<:bleh:1048975096867475537>":
			if randrange(2) == 0:
				await msg.channel.send("<:bleh:1048975096867475537>")
		case "<:cringe:1048975129486569492>":
			if randrange(2) == 0:
				await msg.channel.send("<:cringe:1048975129486569492>")
		case "<:cringeharold:1048975142136598558>":
			if randrange(2) == 0:
				await msg.channel.send("<:cringeharold:1048975142136598558>")
		case "<:doubt:1048975152316157952>":
			if randrange(2) == 0:
				await msg.channel.send("<:doubt:1048975152316157952>")
		case "<:pogchamp:1048975257320575078>":
			if randrange(2) == 0:
				await msg.channel.send("<:pogchamp:1048975257320575078>")
		case "<:weirdchamp:1048975292393332746>":
			if randrange(2) == 0:
				await msg.channel.send("<:weirdchamp:1048975292393332746>")
	# Check for commands.
	await bot.process_commands(msg)



""" TEMPLATE
@bot.command(name = "", description = "")
async def PLACEHOLDER(ctx):
	await ctx.send()
"""
@bot.command(name = "ping", description = "Returns a very helpful message about your ping.")
async def say(ctx):
	await ctx.send(get_random_line_from_file("f_ping.txt"))

@bot.command(name = "info", description = "Returns the most important information about Olaf.")
async def print_info(ctx):
	response = "```\n"
	response += "Bot Name:       " + const.BOT_NAME + "\n"
	response += "App Version:    " + const.APP_VERSION + "\n"
	response += "Lang. Locale:   " + const.LANG_LOCALE + "\n"
	response += "Coding Lang.:   " + const.CODE_LANG + "\n"
	response += "Discord API:    " + const.DISCORD_API + "\n"
	response += "Lines of Code:  " + str(const.CODE_LINES) + "\n"
	response += "```"
	await ctx.send(response)

@bot.command(name = "uptime", description = "Returns the amount of time Olaf has been online for.")
async def uptime(ctx):
	await ctx.send(get_uptime_string())

@bot.command(name = "quote", description = "Returns a random quote from #quotes.")
async def quote(ctx):
	await ctx.send(get_random_line_from_file("f_quotes.txt"))

@bot.command(name = "insult", description = "Returns an extravagant insult for you to use.")
async def insult(ctx):
	await ctx.send(get_random_line_from_file("f_insults.txt"))

@bot.command(name = "fact", description = "Returns a random, useless fact.")
async def funfact(ctx):
	await ctx.send(get_random_line_from_file("f_funfacts.txt"))



@bot.command(name = "timer", description = "Sets a timer for x duration. Syntax: !timer <name> [hh:mm:ss|mm:ss|ss]")
async def add_timer(ctx, name, time_str):
	t_parts = time_str.split(":")
	h, m, s = 0, 0, 0
	match len(t_parts):
		case 1:
			s = int(t_parts[0])
		case 2:
			m, s = int(t_parts[0]), int(t_parts[1])
		case 3:
			h, m, s = int(t_parts[0]), int(t_parts[1]), int(t_parts[2])
		case _:
			await ctx.send('Wrong syntax buddy! Either "hh:mm:ss" or "mm:ss" or "ss".')
	olaf_timer_dict[name] = OlafTimer(ctx.author.id, ctx, h, m, s, name)
	await ctx.send("Timer \"" + name + "\" set for " + prettify_time(0, h, m, s) + ".")

@bot.command(name = "timers", description = "Show a list of all registered timers.")
async def list_timer(ctx):
	if len(olaf_timer_dict) == 0:
		await ctx.send("No active timers.")
	else:
		t = "```\n"
		for key, value in olaf_timer_dict.items():
			t += value.to_string() + "\n"
			#print(value.is_expired())
		t += "```"
		await ctx.send(t)





"""
		MAIN
	----------------------------------------------------------------------------
"""
# Add check_timers() functions to main event loop of pycord
#check_timers.start()

# Run Olaf.
bot.run(TOKEN)
