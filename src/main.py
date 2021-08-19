# TODO ALL OWNER COMMANDS -> check for user id in bot_owner()
# TODO ALL STAFF COMMANDS -> check for user id in bot_staff()

from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from random import randint
from disputils import BotEmbedPaginator

import discord
import dotenv
import datetime
import random
import disputils
import time
import json
import numpy
import os

client = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)
filepath_users = 'users\\users.json'
cards_common = 'cards\\common.json'
cards_uncommon = 'cards\\uncommon.json'
cards_rare = 'cards\\rare.json'
cards_legendary = 'cards\\legendary.json'

start_time = time.time()
load_dotenv()

@client.event
async def on_ready():
    print(f'===================================================')
    print(f'✘  USERNAME: {client.user}')
    print(f'✘  USER_ID:  {client.user.id}')
    print(f'===================================================')

##########################################################################################################
###                                              FUNCTIONS                                             ###
##########################################################################################################

def bot_owner():
    bot_owner_ids = [389897179701182465]
    return (bot_owner_ids)

def bot_staff():
    bot_staff_ids = [389897179701182465]
    return (bot_staff_ids)

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

##########################################################################################################
###                                           OWNER-COMMANDS                                           ###
##########################################################################################################

@client.group(invoke_without_command=True)
async def award(ctx):
    pass

@award.group()
async def balance(ctx, other: discord.Member, amount):
    sent_user = str(other.id)
    sent_amount = int(amount)
    with open(filepath_users, 'r') as f:
        users = json.load(f)
    users[sent_user]['currency'] += sent_amount
    with open(filepath_users, 'w') as f:
        json.dump(users,f, indent=4)
    sent_formatted = ('{:,}').format(sent_amount)
    await ctx.send(f'`{other} has been awarded with ${sent_formatted}`')

##########################################################################################################
###                                           STAFF-COMMANDS                                           ###
##########################################################################################################

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
async def inventory(ctx):
    string_user_id = str(ctx.author.id)
    with open(filepath_users, 'r') as f:
        users = json.load(f)
    if users[string_user_id]['cards']:
        embeds = []
        for card in users[string_user_id]["cards"]:
            if card[-1] == "1":
                with open(cards_common,'r') as co:
                    commonfile = json.load(co)
                card_name = commonfile['common'][card]['name']
                card_source =commonfile['common'][card]['source']
                card_image = commonfile['common'][card]['img']
                card_var = commonfile['common'][card]['event_variant']
                card_rarity = '🃏'
            elif card[-1] == "2":
                with open(cards_uncommon,'r') as co:
                    commonfile = json.load(co)
                card_name = commonfile['uncommon'][card]['name']
                card_source =commonfile['uncommon'][card]['source']
                card_image = commonfile['uncommon'][card]['img']
                card_var = commonfile['uncommon'][card]['event_variant']
                card_rarity = '🃏🃏'
            elif card[-1] == "3":
                with open(cards_rare,'r') as co:
                    commonfile = json.load(co)
                card_name = commonfile['rare'][card]['name']
                card_source =commonfile['rare'][card]['source']
                card_image = commonfile['rare'][card]['img']
                card_var = commonfile['rare'][card]['event_variant']
                card_rarity = '🃏🃏🃏'
            else:
                with open(cards_legendary,'r') as co:
                    commonfile = json.load(co)
                card_name = commonfile['legendary'][card]['name']
                card_source =commonfile['legendary'][card]['source']
                card_image = commonfile['legendary'][card]['img']
                card_var = commonfile['legendary'][card]['event_variant']
                card_rarity = '🃏🃏🃏🃏'
            embeds.append(discord.Embed(title=f"{card_name}", description=f"**Rarity: {card_rarity}**").set_image(url=card_image))
        paginator = BotEmbedPaginator(ctx, embeds)
        return await paginator.run()
    else:
        embed = discord.Embed(description=f'Oops, you don\'t seem to have any cards yet.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='Lorem ipsum dolor sit amet, consectetur adipiscing') 
        await ctx.send(embed=embed)

@client.command()
async def balance(ctx):
    string_user_id = str(ctx.author.id)
    with open(filepath_users,'r') as f:
        users = json.load(f)
    if string_user_id in users:
        balance = users[string_user_id]['currency']
        formatted = ('{:,}').format(balance)
        with open(filepath_users, 'w') as f:
            json.dump(users,f, indent=4)
        embed = discord.Embed(description=f'Your current balance is ${formatted}', colour=discord.Color.from_rgb(0,255,133))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f'Oops, it looks like you don\'t have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !register to create an account.')
        await ctx.send(embed=embed)

###########################################################################################################

client.run(os.getenv('TOKEN_MAIN'))