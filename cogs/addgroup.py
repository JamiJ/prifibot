import discord
from discord.ext import commands
import datetime
import json
import os
import re
import requests


def to_ascii(string):
	string = string.replace("ä", "/ae").replace("ö", "/oe").replace("Ä", "/AE").replace("Ö", "/OE").replace("§", "/ss")
	return string

def to_utf8(string):
	string = string.replace("Ã¤", "ä").replace("Ã¶", "ö").replace("/ae", "ä").replace("/oe", "ö").replace("Ã„", "Ä") \
		.replace("Ã–", "Ö").replace("Â§", "§").replace("/ss", "§")
	return string
	



class CustomGroupsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name="join")
	@commands.guild_only()
	#@commands.has_any_role("raid")
	async def grooauppista(self, ctx, *, arg):
		capsarg = arg.upper()
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		file = f"{path}custom_groups.json"
		role = discord.utils.get(ctx.guild.roles, name=f"{capsarg}")
		user = ctx.message.author
		server = ctx.guild.id
		try:
			with open(file) as data_file:
				data = json.load(data_file)
			if str(capsarg) in list(data[str(server)]):
				#try:
				if role not in user.roles:
					print(f"{user.name} has been added to group {role}")
					await user.add_roles(role)
					await ctx.send(f"Käyttäjä {user.name} lisätty peliporukkaan {role}", delete_after=30.0)
					await ctx.message.add_reaction(":added:543040194689892362")
					return
				#except Exception:
					#print("Error adding")
					#return
					#pass
				#try:
				if role in user.roles:
					print(f"{user.name} has been removed from the group {role}")
					await user.remove_roles(role)
					await ctx.send(f"Käyttäjä {user.name} poistettu peliporukasta {role}", delete_after=30.0)
					await ctx.message.add_reaction(":removed:543039994294697985")
					return
				#except Exception:
					#print("Error removing")
					#return
					#pass
			else:
				await ctx.send(f"Ryhmää {capsarg} ei ole olemassa.", delete_after=30.0)
		except AttributeError:
			pass

	@commands.group(name="group", pass_context=True)
	async def _group(self, ctx):
		""" Tell users what your group command is all about here"""
		if ctx.invoked_subcommand is None:
			print ("Ryhmä komento annettiin ilman alakomentoa")
		
		
		
	#@commands.command(name='group-add', aliases=['lasdadsasdasddasdsa'])
	@_group.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods")
	#async def addcommandgroup(self, ctx, *, arg):
	async def add(self, ctx, *, arg):
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		words = "".join(arg)
		uparg = words.upper()
		file = f"{path}custom_groups.json"
		channel = ctx.channel
		server = ctx.guild.id
		lookr = discord.utils.get(ctx.guild.roles, name = (f"{uparg}"))
		user = ctx.message.author.id
		name = ctx.message.author.name

		if len(uparg) < 1:
			await channel.send("Anna komento sekä ryhmä !group-add osrs", delete_after=30.0)
			#await channel.send(f"{arg}")
			return

		with open(file) as data_file:
			data = json.load(data_file)
		try:
			server_groups = list(data[str(server)])
			if uparg in server_groups:
				await ctx.send(f"Ryhmä `{uparg}` on jo olemassa. Voit liittyä siihen komennolla `!join {uparg}`")
				return
			elif len(server_groups) > 199:
				await channel.send("Ryhmien maksimimäärä on 200", delete_after=30.0)
				return
		except KeyError:
			data[str(server)] = {}
		data[str(server)][uparg] = {"group": uparg}
		with open(file, "w") as data_file:
			json.dump(data, data_file, indent=4)
		await channel.send("Ryhmä `{}` lisätty.".format(to_utf8(uparg)))
		await ctx.guild.create_role(name = f"{uparg}", mentionable=True)


	#@commands.command(name='group-del', aliases=['asddasdsadsaadsadssa'])
	@_group.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods")
	#async def delcommanduus(self, ctx, arg):
	async def remove(self, ctx, arg):
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		channel = ctx.channel
		#group = discord.Role
		server = ctx.guild.id
		file = f"{path}custom_groups.json"
		words = "".join(arg)#.upper() testitssä
		capswords = words.upper()
		print (f"{capswords}")
		try:
			with open(file) as data_file:
				data = json.load(data_file)
			if str(capswords) in list(data[str(server)]):
				del data[str(server)][str(capswords)]
				with open(file, "w") as data_file:
					json.dump(data, data_file, indent=4)
					await channel.send("Ryhmä `{}` poistettu.".format(to_utf8(str(capswords))))
					await capswords.delete()
			else:
				await channel.send("Et voi poistaa tätä ryhmää", delete_after=30.0)
		except AttributeError:
			pass

	#@delcommanduus.error
	#async def delcommanduus_error(self, ctx, error):
	#Tällähetkellä tälle error viestille ei taida olla tarvetta.
	@remove.error
	async def remove_error(self, ctx, error):
		message = ctx.message.content.replace("!group-del ","")
		if isinstance(error, commands.BadArgument):
				return await ctx.send(f"Ryhmää `{message}` ei ole olemassa. Muistithan laittaa ryhmän nimen CAPSILLA: `{message.upper()}` (Korjaus on tulossa).")

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case CommandsCog.
# When we load the cog, we use the name of the file.
def setup(bot):
	bot.add_cog(CustomGroupsCog(bot))


