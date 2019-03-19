import discord
from discord.ext import commands
from discord import Status
import sys
import io
import os
import json
import aiohttp

def to_ascii(string):
	string = string.replace("ä", "/ae").replace("ö", "/oe").replace("Ä", "/AE").replace("Ö", "/OE").replace("§", "/ss")
	return string
			
def to_utf8(string):
	string = string.replace("Ã¤", "ä").replace("Ã¶", "ö").replace("/ae", "ä").replace("/oe", "ö").replace("Ã„", "Ä") \
		.replace("Ã–", "Ö").replace("Â§", "§").replace("/ss", "§")
	return string

def get_prefix(bot, message):
	prefixes = ['!', '>!', '>?']
	if not message.guild:
		return '?'

	return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.owner',
					'cogs.commands',
					'cogs.addcom',
					'cogs.addgroup',
					'cogs.osrs']

bot = commands.Bot(command_prefix=get_prefix, description='A Rewrite Cog Example', case_insensitive=True)
bot.remove_command("help")
# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f'Failed to load extension {extension}.', file=sys.stderr)
			traceback.print_exc()

@bot.event
async def on_member_update(before, after):
	user = before
	strem = discord.utils.get(after.guild.roles, name="Streaming")
	channel = bot.get_channel(236863812651843584)
	if before.activity != after.activity:
		#print(f"{after.name}'s activity changed")
		# Tarkistaa lopettiko käyttäjä aktiviteetin
		try:
			if before.activity.type == 0:
				#print(f"{after.name} stopped playing games")
				#await user.remove_roles(strem)
				pass

			elif before.activity.type == 1:
				print(f"{after.name} stopped streaming to Twitch")
				# await channel.send(f"{after.name} is streaming to Twitch")
				await user.remove_roles(strem)

			elif before.activity.type == 2:
				#print(f"{after.name} stopped listening in Spotify")
				# await user.remove_roles(raid)
				pass
	
		# before.activity == None
		except AttributeError:
			print(f"{after.name} started an activity.")

		# Tarkistaa aloittiko käyttäjä aktiviteetin
		try:
			if after.activity.type == 0:
				#print(f"{after.name} started to play games")
				#await user.remove_roles(strem)
				pass

			elif after.activity.type == 1:
				print(f"{after.name} started streaming to Twitch")
				#await channel.send(f"{after.name} is streaming to Twitch")
				await user.add_roles(strem)
				
			elif after.activity.type == 2:
				#print(f"{after.name} started to listen Spotify")
				# await user.add_roles(raid)
				pass

		# after.activity == None
		except AttributeError:
			print(f"{after.name} stopped all activities.")

@bot.event
async def on_member_join(user):
	channel = bot.get_channel(236863812651843584)
	await channel.send(f'{user.name} liittyi kanavalle 👋🏼')
	
	
@bot.event
async def on_member_remove(user):
	channel = bot.get_channel(236863812651843584)
	await channel.send(f'{user.name} poistui kanavalta 👋🏼')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    await bot.change_presence(activity=discord.Activity(name="PRI-FI Bot by Fusious#7927", type=0))

bot.aiohttp_session = aiohttp.ClientSession(loop=bot.loop)
bot.run("TOKEN", bot=True, reconnect=True)


