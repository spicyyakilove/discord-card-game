from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from random import randint

import discord
import dotenv
import datetime
import random
import time
import json
import numpy
import os

client = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)
filepath_users = 'users\\users.json'
start_time = time.time()
load_dotenv()

def pre_alpha_testers():
	pre_alpha_ids = [389897179701182465]
	return (pre_alpha_ids)

def bot_staff():
	bot_staff_ids = [389897179701182465]
	return (bot_staff_ids)

@client.event
async def on_ready():
	print(f'===================================================')
	print(f'✘  USERNAME: {client.user}')
	print(f'✘  USER_ID:  {client.user.id}')
	print(f'===================================================')

##########################################################################################################
###                                           OWNER-COMMANDS                                           ###
##########################################################################################################

@client.group(invoke_without_command=True)
@commands.is_owner()
async def award(ctx):
	pass

@award.group()
@commands.is_owner()
async def balance(ctx, other: discord.Member, amount):
	sent_user = str(other.id)
	sent_amount = int(amount)
	with open(filepath_users, 'r') as f:
		users = json.load(f)
	users[sent_user]['currency'] += sent_amount
	with open(filepath_users, 'w') as f:
		json.dump(users,f, indent=4)
	
	await ctx.send(f'{sent_amount} has been gifted to {other.mention}')

@award.group()
@commands.is_owner()
async def card(ctx, other: discord.Member, card):
	pass

##########################################################################################################
###                                           STAFF-COMMANDS                                           ###
##########################################################################################################

# TODO bot -> check for user id in bot_staff()
# TODO status <group> -> check for user id in bot_staff()

@client.command()
async def bot(ctx):
	global startTime
	uptime = str(datetime.timedelta(seconds=int(round(time.time()-start_time))))
	await ctx.send(f'`Status: Online | Ping: {round(client.latency * 1000)}ms | Uptime: {uptime}`')

@client.group(invoke_without_command=True)
async def status(ctx):
	await client.change_presence(status=None)
	await ctx.send('`Status cleared`')

@status.group()
async def playing(ctx, *, status):
	await client.change_presence(activity=discord.Game(name=f'{status}'))
	await ctx.send(f'`Status set as Playing {status}`')

@status.group()
async def watching(ctx, *, status):
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{status}'))
	await ctx.send(f'`Status set as Watching {status}`')

@status.group()
async def listening(ctx, *, status):
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{status}'))
	await ctx.send(f'`Status set as Listening to {status}`')

@status.group()
async def streaming(ctx, *, status):
	await client.change_presence(activity=discord.Streaming(name=f'{status}', url='https://www.twitch.tv/pokimane'))
	await ctx.send(f'`Status set as Streaming {status}`')

@status.group()
async def competing(ctx, *, status):
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f'{status}'))
	await ctx.send(f'`Status set as Competing in {status}`')

###########################################################################################################
###                                           USER-COMMANDS                                             ###
###########################################################################################################

@client.command()
async def register(ctx):
	string_user_id = str(ctx.author.id)
	with open(filepath_users, 'r') as f:
		users = json.load(f)
	if string_user_id not in users:
		users[string_user_id] = {}
		users[string_user_id]['currency'] = 100
		users[string_user_id]['cards'] = []
		users[string_user_id]['cooldown'] = '01-Jan-2020'
		users[string_user_id]['blacklist'] = False
		with open(filepath_users, 'w') as f:
			json.dump(users,f, indent=4)
		embed = discord.Embed(description=f'Congratulations, your account has been successfully created.', colour=discord.Color.from_rgb(0,255,133))
		embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
		embed.set_footer(text='You can use !help to see a full list of commands.')
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(description=f'Oops, it looks like you already have an account.', colour=discord.Color.from_rgb(225,29,98))
		embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
		embed.set_footer(text='You can use !help to see a full list of commands.')
		await ctx.send(embed=embed)

@client.command()
async def balance(ctx):
	string_user_id = str(ctx.author.id)
	with open(filepath_users,'r') as f:
		users = json.load(f)
	balance = users[string_user_id]['currency']
	formatted = ('{:,}').format(balance)
	with open(filepath_users, 'w') as f:
		json.dump(users,f, indent=4)
	embed = discord.Embed(description=f'Your current balance is ${formatted}', colour=discord.Color.from_rgb(0,255,133))
	embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
	await ctx.send(embed=embed)

##########################################################################################################
###                                           TESTER-COMMANDS                                          ###
##########################################################################################################

# TODO check_card_algorithm -> check for user id in pre_alpha_testers()
# TODO check_balance_algorithm -> check for user id in pre_alpha_testers()

@client.command()
async def check_card_algorithm(ctx):
	result = card_algorithm()
	embed = discord.Embed(description=f'{result}', colour=discord.Color.from_rgb(0,0,0))
	embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
	await ctx.send(embed=embed)

@client.command()
async def check_balance_algorithm(ctx):
	result = balance_algorithm()
	embed = discord.Embed(description=f'{result}', colour=discord.Color.from_rgb(0,0,0))
	embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
	await ctx.send(embed=embed)

###########################################################################################################
###                                          ERROR-HANDLING                                             ###
###########################################################################################################

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(description='Oops, this command is only supposed to be used by owner.', colour=discord.Color.from_rgb(225,29,98))
		await ctx.send(embed=embed)

###########################################################################################################
###                                            ALGORITHMS                                               ###
###########################################################################################################

def card_algorithm():
	random_number = numpy.random.randint(low=0, high=100, size=1)
	if random_number <= 2:
		result = 'legendary'
	elif 2 < random_number <= 8:
		result = 'rare'
	elif 8 < random_number <= 25:
		result = 'uncommon'
	else:
		result = 'common'
	return(result)

def balance_algorithm():
	random_number = numpy.random.randint(low=0, high=100, size=1)
	if random_number <= 2:
		result = 650
	elif 2 < random_number <= 8:
		result = 250
	elif 8 < random_number <= 25:
		result = 80
	else:
		result = 20
	return(result)

client.run(os.getenv('TOKEN_MAIN'))