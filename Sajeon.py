#############################################################################
# Sajeon Bot created by Joshua Choe (Caesura#5738)							#
# Bot 'frame' was used from the Discord Bot Tutorial from HABchy #1665		#
#																			#
# I made this as a fun project to do over the winter break.					#
# It seemed like there was a need for a korean dictionary bot for discord 	#
# that wasn't being met, so just thought I might as well make one myself	#
#############################################################################


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
client = Bot(description="Use '^dic or ^얓 ___' to summon a definition from naver!", command_prefix="^", pm_help = True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=117824'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('Bot Tutorial created by Habchy#1665')
	print('Sajeon created by Caesura#5738')
	print()

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def dic(*args):

	# Pretty sure theres a better way to do this, but this just concatenates a query with more than one word
	if args:
		if len(args) > 1:
			query = " ".join(args)
		elif len(args) == 1:
			query = args[0]

		#Detects the language of the query
		lang = detect(query)

		#If the language detected is Korean then we are translating Korean to English
		if lang == "ko":
			# Sets search_url as the url that would search naver for the word
			search_url = "http://endic.naver.com/search.nhn?sLn=kr&searchOption=all&query=" + quote(query)

			# Initialize the parallel lists that we will use
			listing_list = []
			hanja_list = []
			detail_link_list = []
			definition_list = []
			kr_ex_sent_list = []
			en_ex_sent_list = []


			# Opens the search page from search_url and uses BeautifulSoup to get the html for it.
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

					# Appends the hanja for the word (if it exists), Note only the first entry usually has hanja
					if header.contents[2]:
						hanja_list.append(header.contents[2].strip())
					else:
						hanja_list.append("")
					
				#This is the overall html block that contains the definition and example sentences
				for block in soup.find_all('div', class_='align_right'):
					definition_list.append(block.find('span', class_='fnt_k05').text)

					# If the korean example sentence is able to be found, append it
					if block.find('span', class_='fnt_e07 _ttsText'):
						kr_ex_sent_list.append(block.find('span', class_='fnt_e07 _ttsText').text)
					else:
						kr_ex_sent_list.append("")

					# If the english example sentence is able to be found, append it
					if block.find('span', class_='fnt_k10 _ttsText'):
						en_ex_sent_list.append(block.find('span', class_='fnt_k10 _ttsText').text)
					else:
						en_ex_sent_list.append("")

			response.close()

			# Checks to make sure that the very first entry has a value (aka an example sentence)
			# If not, then we output 'no example sentence'
			# If so, then we output the sentence
			if kr_ex_sent_list[0] == "":
				single_output = """**[{0}:]({1})** {2} {3}\n\t*No example sentence.*""".format(listing_list[0],detail_link_list[0],hanja_list[0],definition_list[0])
			else:
				single_output = """**[{0}:]({1})** {2} {3}\n\t*{4}*\n\t*{5}*""".format(listing_list[0],detail_link_list[0],hanja_list[0],definition_list[0],kr_ex_sent_list[0],en_ex_sent_list[0])

			# Sets up the embed and outputs it to discord
			embed_title = "Results for {0}".format(query)
			simple_em = discord.Embed(title=embed_title, description=single_output, url=search_url, colour=discord.Colour.red())
			await client.say(embed=simple_em)

		#then we are translating English to Korean
		elif query.isalpha() == True:
			


			await client.say("Translating English to Korean")

		else:
			await client.say("Invalid input or a non Korean/English language! Please try again.")

# Same method, but allowing for the korean equivalent of typing 'dic' but on a korean keyboard
@client.command()
async def 얓(*args):

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
			hanja_list = []
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

					if header.contents[2]:
						hanja_list.append(header.contents[2].strip())
					else:
						hanja_list.append("")
					
					#get the link to show more definitions for each on of these

				for block in soup.find_all('div', class_='align_right'):
					definition_list.append(block.find('span', class_='fnt_k05').text)

					if block.find('span', class_='fnt_e07 _ttsText'):
						kr_ex_sent_list.append(block.find('span', class_='fnt_e07 _ttsText').text)
					else:
						kr_ex_sent_list.append("")

					if block.find('span', class_='fnt_k10 _ttsText'):
						en_ex_sent_list.append(block.find('span', class_='fnt_k10 _ttsText').text)
					else:
						en_ex_sent_list.append("")

			response.close()

			if kr_ex_sent_list[0] == "":
				single_output = """**[{0}:]({1})** {2} {3}\n\t*No example sentence.*""".format(listing_list[0],detail_link_list[0],hanja_list[0],definition_list[0])
			else:
				single_output = """**[{0}:]({1})** {2} {3}\n\t*{4}*\n\t*{5}*""".format(listing_list[0],detail_link_list[0],hanja_list[0],definition_list[0],kr_ex_sent_list[0],en_ex_sent_list[0])
			#simple_output = """**[{2}:]({6})** {3}\n\t*{4}*\n\t*{5}*\n---\n**[{7}:]({11})** {8}\n\t*{9}*\n\t*{10}*""".format(query,search_url,listing_list[0],definition_list[0],kr_ex_sent_list[0],en_ex_sent_list[0],detail_link_list[0],listing_list[1],definition_list[1],kr_ex_sent_list[1],en_ex_sent_list[1],detail_link_list[1])

			embed_title = "Results for {0}".format(query)

			simple_em = discord.Embed(title=embed_title, description=single_output, url=search_url, colour=discord.Colour.red())


			await client.say(embed=simple_em)

			#await client.say(url) #get a url shortener

		elif query.isalpha() == True:
			#then we are translating English to Korean


			await client.say("Translating English to Korean")

		else:
			await client.say("Invalid input or a non Korean/English language! Please try again.")
# After you have modified the code, feel free to delete the line above (line 33) so it does not keep popping up everytime you initiate the ping commmand.
	
client.run('Mzk2MDAxNDU4ODUzNzczMzEy.DSbEnw.dM4dlOK0kyQmUllobxy8TF2FCbg')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.