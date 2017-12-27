# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
from urllib.request import urlopen
from langdetect import detect
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Use '.kdic ___' to summon a definition from naver!", command_prefix="^", pm_help = True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('Created by Habchy#1665')
	print()
	print()

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def dic(*args):

	if args:
		if len(args) > 1:
			query = " ".join(args)
		elif len(args) == 1:
			query = args[0]

		lang = detect(query)

		if lang == "ko":
			# Then we are translating Korean to English
			search_url = "http://endic.naver.com/search.nhn?sLn=kr&searchOption=all&query=" + quote(query)

			listing_list = []
			detail_link_list = []
			definition_list = []
			kr_ex_sent_list = []
			en_ex_sent_list = []


			with urllib.request.urlopen(search_url) as response:
				soup = BeautifulSoup(response.read(), "html.parser")
				
				for header in soup.find_all('span', class_='fnt_e30'):

					# This try except block appends the actual word
					try:
						listing_list.append(header.find('a').text)
					except:
						listing_list.append(None)

					# This appends the link for each word that will go to their detailed page
					detail_link_list.append("http://endic.naver.com" + header.find('a')['href'])

					#get the link to show more definitions for each on of these

				for definition in soup.find_all('span', class_='fnt_k05'):
					definition_list.append(definition.text)


				for kr_ex_sent in soup.find_all('span', class_='fnt_e07 _ttsText'):
					kr_ex_sent_list.append(kr_ex_sent.text)


				for en_ex_sent in soup.find_all('span', class_='fnt_k10 _ttsText'):
					en_ex_sent_list.append(en_ex_sent.text)

			response.close()



			simple_output = """**[{2}:]({6})** {3}\n\t*{4}*\n\t*{5}*\n---\n**[{7}:]({11})** {8}\n\t*{9}*\n\t*{10}*""".format(query,search_url,listing_list[0],definition_list[0],kr_ex_sent_list[0],en_ex_sent_list[0],detail_link_list[0],listing_list[1],definition_list[1],kr_ex_sent_list[1],en_ex_sent_list[1],detail_link_list[1])

			embed_title = "Results for {0}".format(query)

			simple_em = discord.Embed(title=embed_title, description=simple_output, url=search_url, colour=discord.Colour.red())


			await client.say(embed=simple_em)

			#await client.say(url) #get a url shortener

		elif query.isalpha() == True:
			#then we are translating English to Korean


			await client.say("Translating English to Korean")

		else:
			await client.say("Only English and Korean are supported! Please try again.")

	#query now holds the data we need to look up


	#url = 'http://endic.naver.com/search.nhn?sLn=kr&isOnlyViewEE=N&query={0}'.format(args) # write the url here

	#usock = urlopen(url)
	#data = usock.read()

	

	#usock.close()

	#await client.say(":ping_pong: Pong!")
	#await asyncio.sleep(3)
# After you have modified the code, feel free to delete the line above (line 33) so it does not keep popping up everytime you initiate the ping commmand.
	
client.run('MzkzODg5Mzg4MDQxNDY5OTYy.DR8Vow.TdKrp-NpkXVVYVGT3UW6qDoGzpU')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.