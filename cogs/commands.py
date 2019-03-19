# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import sys
import requests
from bs4 import BeautifulSoup
from discord.ext.commands.cooldowns import BucketType
import os
import aiohttp
import random


class CommandsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	async def visit_website(self, link: str, encoding="utf-8", timeout=5):
		try:
			async with self.bot.aiohttp_session.get(link, timeout=timeout) as r:
				resp = await r.text(encoding=encoding)
			return resp
		except aiohttp.ServerTimeoutError:
			print("TimeoutError")
			return
		
	@commands.group(name="help", pass_context=True)
	async def _help(self, ctx):
		""" Tell users what your group command is all about here"""
		if ctx.invoked_subcommand is None:
			embed=discord.Embed(title="-----------------------------------------", color=0xff0000)
			embed.set_author(name="Help")
			embed.add_field(name="!commands", value="Shows available commands", inline=True)
			embed.add_field(name="!patchnotes", value="Bot's latest updates", inline=False)
			embed.add_field(name="!help custom", value="Custom commands help", inline=False)
			embed.set_footer(text="Development version")		
			await ctx.send(embed=embed, delete_after=60)
			await ctx.message.delete()
		
	#@commands.command(name='help-custom', aliases=['juuheliks'])
	@_help.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods", "raid")
	#async def helpcustom(self, ctx):
	async def custom(self, ctx):
		embed=discord.Embed(title="-----------------------------------------", color=0xff0000)
		embed.set_author(name="Custom commands")
		embed.add_field(name="!command add", value='!command add test "text"', inline=True)
		embed.add_field(name="!command remove", value='!command remove test', inline=True)
		embed.set_footer(text="Use added commands with $ | $test | Development version")
		await ctx.send(embed=embed, delete_after=60.0)
		await ctx.message.delete()
		
	@commands.group(name="region", pass_context=True)
	async def _region(self, ctx):
		""" Tell users what your group command is all about here"""
		if ctx.invoked_subcommand is None:
			embed=discord.Embed(title="-----------------------------------------", color=0xff0000)
			embed.set_author(name="Help")
			embed.add_field(name="!commands", value="Shows available commands", inline=True)
			embed.add_field(name="!patchnotes", value="Bot's latest updates", inline=False)
			embed.add_field(name="!help custom", value="Custom commands help", inline=False)
			embed.set_footer(text="Development version")		
			await ctx.send(embed=embed, delete_after=60)
			await ctx.message.delete()
		
	@_region.command()
	@commands.guild_only()
	@commands.has_any_role("Admins", "Mods", "raid")
	@commands.cooldown(1, 900, BucketType.guild) 
	# Limit how often a command can be used, (num per, seconds, Buckettype.default/user/server/channel)
	#regions: amsterdam, brazil, eu_central, eu_west, frankfurt, hongkong, japan, london, russia
	#regions: singapore, southafrica, sydney, us_central, us_east, us_south, us_west, 
	async def change(self, ctx):
		list = ["russia", "eu-central", "eu-west"]
		#print(ctx.guild.region)
		#await ctx.send(ctx.guild.region)
		region = str(ctx.guild.region)
		try:
			if region == str("russia"):
				print("Server region changed to eu-west")
				await ctx.send("Server region changed to `eu-west`")
				await ctx.guild.edit(region="eu-west")
				await ctx.message.delete()
			elif region == str("eu-west"):	
				print("Server region changed to  eu-central")
				await ctx.send("Server region changed to `eu-central`")
				await ctx.guild.edit(region="eu-central")
				await ctx.message.delete()
			elif region == str("eu-central"):
				print("Server region changed to russia")
				await ctx.send("Server region changed to `russia`")
				await ctx.guild.edit(region="russia")
				await ctx.message.delete()
			else:
				print("Palvelinta ei ole")
				print(ctx.guild.region)
				await ctx.message.delete()
				return
		except NameError:
			pass
			return

	@commands.command(name='patchnotes', aliases=['pn'])
	@commands.guild_only()
	async def patchnotes(self, ctx):
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		with open(f"{path}changelog.txt", "r", encoding="utf-8") as file:
			changelog = file.read()
		embed = discord.Embed(title="Latest changes", description=changelog, color=0xff0000)
		await ctx.send(embed=embed, delete_after=60)
		await ctx.message.delete()
	
	@commands.command(name='commands', aliases=['komennot'])
	@commands.guild_only()
	async def commmands(self, ctx):
		path = "{}/customfiles/".format(os.path.dirname(__file__))
		if path == "/":
			path = ""
		with open(f"{path}commands.txt", "r", encoding="utf-8") as file:
			changelog = file.read()
		embed = discord.Embed(title="All the available commands for the bot.", description=changelog, color=0xff0000)
		await ctx.send(embed=embed, delete_after=60.0)
		await ctx.message.delete()

	@commands.command(name="info", aliases=['kuinkakauanolenollutdiscordissa', 'whenautismstart', 'whenmysociallifeended', 'joined', 'liittymisaika'])
	@commands.guild_only()
	@commands.cooldown(1,5,BucketType.user)
	# Limit how often a command can be used, (num per, seconds, Buckettype.default/user/guild/channel)
	async def info(self, ctx):
		user = ctx.message.author
		embed = discord.Embed(title="{}'s info".format(user.name), color=0x00ff00) #description="Here's what I could find."
		embed.add_field(name="Name", value=user.name, inline=True)
#		embed.add_field(name="Highest role", value=user.top_role)
		embed.add_field(name="Joined", value=user.joined_at)
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=embed, delete_after=60.0)
		await ctx.message.delete()

	@commands.command()
	@commands.guild_only()
	async def miekka(self, ctx):
		user = ctx.message.author
		await ctx.send(f"{user.name} <:Attack_icon:548862941873831962>", delete_after=30.0)
		await ctx.message.delete()

	@commands.command()
	@commands.guild_only()
	async def kruunu(self, ctx):
		user = ctx.message.author
		await ctx.send(f"{user.name} 👑", delete_after=30.0)
		await ctx.message.delete()

		
	#Koodia lainattu, mutta kirjoitettu rewriten kanssa toimivaksi. https://github.com/Visperi/OsrsHelper 
	@commands.command(name='vanhaupdate', aliases=['vanhaupdateosrs'])
	@commands.guild_only()
	async def latest_update(self, ctx):
		dates = []
		news_html = []
		article_numbers = []
		channel = ctx.guild.get_channel(407630051127984130)
		link = "http://oldschool.runescape.com/"
		try:
			html = requests.get(link, timeout=4).text
		except requests.exceptions.ReadTimeout:
			await channel.send("Sivu ei vastaa!")
			return
		try:
			html_parsed = BeautifulSoup(html, "html.parser")
			for i in html_parsed.findAll("time"):
				if i.has_attr("datetime"):
					dates.append(i["datetime"])
			latest_date = max(dates)
										#Hakee div classista news-article detailit
			for j in html_parsed.find_all("div", attrs={"class": "news-article__details"}):
				if j.find("time")["datetime"] == latest_date:
					news_html.append(j.find("p"))
										#Appendaa artikkeli linkit järjestykseen
			for k in news_html:				
				article_number = int(k.find("a")["id"].replace("news-article-link-", ""))
				article_numbers.append(article_number)
			min_article_nr = min(article_numbers)
										#Hakee viimisimmän artikkelin ja postaa sen kanavalle.
			for l in news_html:
				article_number = int(l.find("a")["id"].replace("news-article-link-", ""))
				if article_number == min_article_nr:
					news_link = l.find("a")["href"]
					await channel.send(f"Old School RuneScape's latest updates {news_link}")
					await ctx.message.delete()
					return
		except AttributeError:
				pass
				
	#Koodia lainattu, mutta kirjoitettu rewriten kanssa toimivaksi. https://github.com/Visperi/OsrsHelper
	@commands.command(name='wiki', aliases=['wikii'])
	@commands.guild_only()
	async def search_wiki(self, message, *, arg):
		baselink = "https://oldschool.runescape.wiki/w/"								#Linkki minkä perään lisätään hakusanat
		channel = message.guild.get_channel(407630051127984130)							#Kanava millä tämä komento toimii
		search = "".join(arg).replace(" ", "_")											#Haku, missä haetaan hakusanat perään
		search_link = baselink + search													#Yhdistetään linkki ja hakusanat
		response = requests.get(search_link).text										#Haetaan vastaus, hakusanoilla tehdystä linkistä
		if f"This page doesn&#039;t exist on the wiki. Maybe it should?" in response:
			hyperlinks = []
			truesearch_link = f"https://oldschool.runescape.wiki/w/Special:Search?search={search}"
			truesearch_resp = requests.get(truesearch_link).text

			# parse html
			results_html = BeautifulSoup(truesearch_resp, "html.parser")
			result_headings = results_html.findAll("div", class_="mw-search-result-heading")
			if len(result_headings) == 0:
				await channel.send("Hakusanalla/hakusanoilla ei löytynyt yhtään sivua.")
				await message.message.delete()
				return
			for result in result_headings[:5]:
				link_end = result.find("a")["href"]
				link_title = result.find("a")["title"]
				hyperlinks.append(f"[{link_title}](https://oldschool.runescape.wiki{link_end})")
			embed = discord.Embed(title="Mahdollinen lista tuloksista", color=6564126, description="\n".join(hyperlinks))
			await channel.send(embed=embed, delete_after=300.0)
			await message.message.delete()
		else:
			await channel.send(f"<{search_link}>", delete_after=500.0)
			await message.message.delete()
			
	@commands.command(name="update")
	@commands.guild_only()
	async def osrs_latest_news(self, ctx):
		"""
		Parse Old School Runescape homepage for latest game and community news and send a links to them.
		:param ctx:
		:return:
		"""
		channel = ctx.guild.get_channel(407630051127984130)#407630051127984130
		game_articles = {}
		community_articles = {}

		try:
			if ctx.message.channel == channel:
				link = "http://oldschool.runescape.com/"
				osrs_response = await self.visit_website(link)
				osrs_response_html = BeautifulSoup(osrs_response, "html.parser")
				
				for div_tag in osrs_response_html.findAll("div", attrs={"class": "news-article__details"}):
					p_tag = div_tag.p
					# Somehow the article types always end in space so leave it out
					article_type = div_tag.span.contents[0][:-1]
					article_link = p_tag.a["href"]
					article_number = p_tag.a["id"][-1]
					if article_type == "Game Updates":
						game_articles[article_number] = article_link
					elif article_type == "Community":
						community_articles[article_number] = article_link

				# Find the smallest article numbers for both article types
				min_article_game = min(game_articles.keys())
				min_article_community = min(community_articles.keys())

				game_link = game_articles[min_article_game]
				community_link = community_articles[min_article_community]

				await channel.send(f"Uusimmat tapahtumat Old School Runescapessa.\n\n"
								f"Pelin päivitykset: {game_link}\n"
								f"Yhteisön päivitykset: {community_link}", delete_after=300.0)
				await ctx.message.delete()
			elif ctx.message.channel != channel:
				await ctx.send("Et voi käyttä `!update` komentoa tällä kanavalla. Komento toimii vain `#RS` kanavalla", delete_after=20.0)
				await ctx.message.delete()
			else:
				print("Every broke")
		except NameError:
			pass

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 10, BucketType.user) 
	# Limit how often a command can be used, (num per, seconds, Buckettype.default/user/guild/channel)
	async def kissu(self, ctx):
		r = requests.get('https://aws.random.cat/meow')
		cat = str(r.json()['file'])
		embed = discord.Embed(title="", colour=0x03C9A9)
		embed.set_image(url=cat)
		#print(ctx.message.mentions)
		if ctx.message.role_mentions:
			await ctx.message.delete()
		elif ctx.message.mentions:
			await ctx.message.delete()
		else:
			await ctx.send(embed=embed, delete_after=25.0) 
			await ctx.message.delete()
			
	@kissu.error
	async def kissu_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
				await ctx.message.delete()
				#return await ctx.send(f"Olet tällä hetkellä jäähyllä ", delete_after=10.0)
				return
				
# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case CommandsCog.
# When we load the cog, we use the name of the file.
def setup(bot):
	bot.add_cog(CommandsCog(bot))

