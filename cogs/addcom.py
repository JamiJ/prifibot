import discord
from discord.ext import commands
import sys
import io
import os
import json
import datetime
import re
import requests


def to_ascii(string):
	string = string.replace("ä", "/ae").replace("ö", "/oe").replace("Ä", "/AE").replace("Ö", "/OE").replace("§", "/ss")
	return string
			
def to_utf8(string):
	string = string.replace("Ã¤", "ä").replace("Ã¶", "ö").replace("/ae", "ä").replace("/oe", "ö").replace("Ã„", "Ä") \
		.replace("Ã–", "Ö").replace("Â§", "§").replace("/ss", "§")
	return string

	
class CustomCommandsCog(commands.Cog):#discord.Client
	def __init__(self, bot):
		self.bot = bot
		
	@commands.group(name="command", pass_context=True)
	async def _command(self, ctx):
		""" Tell users what your group command is all about here"""
		if ctx.invoked_subcommand is None:
			print ("Komento annettiin ilman alakomentoa")
			await ctx.send("`!command add/remove hi ""\"hello""\"`", delete_after=30.0)
			
	#listeners now must have a decorator
	@commands.Cog.listener()
	async def on_message(self, message):
		guild = message.guild
		channel = message.channel
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		try:
			if message.content.startswith('!'):
				if guild:
					with open("{}chatlogs/{}.txt".format(path, guild.name), "a+", encoding="utf-8") as logs:
						print(to_utf8(str(("{0.created_at} : {0.author.name} : {0.channel} : {0.content} : {0.embeds}".format(message)))), file=logs)
				try:
					server = message.guild.id
				except AttributeError:
					return
				command = message.content.replace("!", "")
				#print (command)
				try:
					with open(f"{path}custom_commands.json") as data_file:
						data = json.load(data_file)
						#print("Tiedosto avattu")
					try:
						viesti = data[str(server)]["!{}".format(to_ascii(str(command)))]["message"]
						await channel.send(to_utf8(viesti), delete_after=300.0)
						
						return
					except KeyError: #NameError for fixing, if command manage to go broken
						return
						print("Viestin sanomisessa KeyError / path on väärin merkitty")
				except IOError:
					print ("Tiedoston avaamisessa on vikaa, path on väärin")
					return
			else:
				#print("Viesti ei alkanut '!' merkillä")
				#print("Poistetaan käyttäjän lähettämä viesti")
				#await self.message.delete()
				#await bot.process_commands(message)
				pass
				#return
		except AttributeError:
			#print("Komento aloitettiin väärin!")
			pass
		
		
	#@commands.command(name='command-add', aliases=['lisaa'])
	@_command.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods", "raid")
	async def add(self, message, *, arg):
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		words = "".join(arg)#.replace(" ", " ")	
		file = f"{path}custom_commands.json"
		#channel = message.guild.get_channel(521118811198586891)
		channel = message.channel
		server = message.guild.id
		
		if len(words) < 3:
			await channel.send("Anna komento, sekä viesti: `!command add hi ""\"hello""\"`", delete_after=40.0)
			#await channel.send(f"{arg}")
			return
			
		def convert(string):
			a = string.find("\"")
			if a == -1 or string[-1] != "\"" or string.count("\"") < 2:
				return
			string_list = list(string)
			string_list[a], string_list[-1] = "[start]", "[end]"
			if string_list[a - 1] != " ":
				string_list[a - 1] += " "
			string = "".join(string_list)
			start = string.find("[start]") + 7
			end = string.find("[end]")
			viesti_raw = to_ascii(string[start:end]).replace("\\n", "\n")
			komento_raw = to_ascii(" ".join(string[:start - 8].split(" ")[0:]))
			komento = komento_raw.replace("!", "")
			try:
				if not komento[0].isalpha() and not komento[0].isdigit():
					komento = list(komento)
					komento[0] = "!"
					komento = "".join(komento)
				elif komento[0].isalpha() or komento[0].isdigit():
					komento = "!" + komento
				return komento.lower(), viesti_raw, komento_raw
			except IndexError:
				raise IndexError
		try:
			command, viesti, command_raw = convert(words)
			if len(command_raw) > 30:
				raise ValueError
			if "[end]" in command and "[start]" in command:
				await channel.send("Annoit vääränlaisen syötteen. Anna ensin komento ja sitten "
														   "viesti lainausmerkeissä.", delete_after=40.0)
				return
		except TypeError:
			await channel.send("Komennon viestin täytyy alkaa ja päättyä lainausmerkillä. "
													   "Anna ensin komento ja sitten viesti."
													   "`!command add hi ""\"hello""\"`", delete_after=40.0)
			return
		except IndexError:
			await channel.send("Komennon nimi ei saa olla pelkkiä huutomerkkejä, sillä ne "
													   "poistetaan siitä joka tapauksessa. Siten tämä komento olisi "
													   "tyhjä merkkijono.", delete_after=40.0)
			return
		except ValueError:
			await channel.send(f"Komennon maksimipituus on 30 merkkiä. Sinun oli "f"{len(command_raw)}.", delete_after=30.0)
			return
		with open(file) as data_file:
			data = json.load(data_file)
		try:
			server_commands = list(data[str(server)])
			if command in server_commands:
				await channel.send("Komento on jo olemassa.", delete_after=40.0)
				return
			elif len(server_commands) > 199:
				await channel.send("Komentojen maksimimäärä on 200 kappaletta, joka on tällä "
														   "guildilla jo täyttynyt.", delete_after=40.0)
				return
		except KeyError:
			data[str(server)] = {}
		data[str(server)][command] = {"message": viesti}
		with open(file, "w") as data_file:
			json.dump(data, data_file, indent=4)
		await channel.send("Komento `{}` lisätty.".format(to_utf8(command)), delete_after=40.0)
		await message.message.delete()
		if (command_raw[0] == "!" and command_raw.count("!") > 1) or (command_raw[0] != "!" and command_raw.count("!") > 0):
			#await channel.send("Komennon nimessä ei voi olla huutomerkkejä ja ne poistettiin automaattisesti.")
			print ("Komennon nimessä ei voi olla dollarin merkkejä ja ne poistettiin automaattisesti.")

	#@commands.command(name='command-del', aliases=['poista', 'remove'])
	@_command.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods", "raid")
	async def remove(self, message, *, arg):
		#channel = message.guild.get_channel(521118811198586891)
		channel = message.channel
		komento = " ".join(arg).replace(" ", "")
		server = message.guild.id
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		file = f"{path}custom_commands.json"
		if not komento[0].isalpha() and not komento[0].isdigit():
			komento = list(komento)
			komento[0] = "!"
			komento = "".join(komento)
		elif komento[0].isalpha() or komento[0].isdigit():
			komento = "!" + komento
		komento = to_ascii(komento)
		with open(file) as data_file:
			data = json.load(data_file)
		if str(komento) in list(data[str(server)]):
			del data[str(server)][str(komento)]
			with open(file, "w") as data_file:
				json.dump(data, data_file, indent=4)
				await channel.send("Komento `{}` poistettu.".format(to_utf8(str(komento))), delete_after=40.0)
				await message.message.delete()
		else:
			await channel.send(f"Komentoa `{arg}` ei ole olemassa.", delete_after=40.0)
			await message.message.delete()
		
# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case CommandsCog.
# When we load the cog, we use the name of the file.
def setup(bot):
	bot.add_cog(CustomCommandsCog(bot))

