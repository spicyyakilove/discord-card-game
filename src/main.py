###########################################################################################################
###     SETUP                                                                                           ###
###########################################################################################################

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

filepath_player_0 = 'users\\users.json'
filepath_rarity_1 = 'cards\\rarity1.json'
filepath_rarity_2 = 'cards\\rarity2.json'
filepath_rarity_3 = 'cards\\rarity3.json'
filepath_rarity_4 = 'cards\\rarity4.json'

start_time = time.time()
load_dotenv()

###########################################################################################################
###     FUNCTIONS                                                                                       ###
###########################################################################################################



def card_algorithm_1():
    random_number = numpy.random.randint(low=0, high=100, size=1)
    if random_number <= 2:
        result = 'rarity4'
    elif 2 < random_number <= 10:
        result = 'rarity3'
    elif 10 < random_number <= 35:
        result = 'rarity2'
    elif 35 < random_number:
        result = 'rarity1'
    return(result)



def card_algorithm_2():
    random_number = numpy.random.randint(low=0, high=100, size=1)
    if random_number <= 5:
        result = 'rarity4'
    elif 5 < random_number <= 20:
        result = 'rarity3'
    elif 20 < random_number <= 45:
        result = 'rarity2'
    elif 45 < random_number:
        result = 'rarity1'
    return(result)



def balance_algorithm():
    random_number = numpy.random.randint(low=0, high=100, size=1)
    if random_number <= 2:
        result = 650
    elif 2 < random_number <= 8:
        result = 250
    elif 8 < random_number <= 25:
        result = 80
    elif 25 < random_number:
        result = 20
    return(result)



def random_card(card_rarity):
    file_name = card_rarity + '.json'
    with open('cards\\' + file_name) as file:
        card_data = json.load(file)
    card_list = card_data[card_rarity]
    pick_code = random.choice(list(card_list.keys()))
    card_name = card_list[pick_code]['name']
    card_image = card_list[pick_code]['image']
    card_code = pick_code
    return(card_name, card_code, card_image)



def add_card(ctx, card_code):
    string_user_id = str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    users[string_user_id]['cards'].append(card_code)
    with open(filepath_player_0, 'w') as file:
        json.dump(users, file, indent=4)



###########################################################################################################
###     COMMANDS                                                                                        ###
###########################################################################################################



@client.command()
async def register(ctx):
    string_user_id = str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    if string_user_id not in users:
        users[string_user_id] = {}
        users[string_user_id]['currency'] = 100
        users[string_user_id]['cards'] = []
        users[string_user_id]['cooldown'] = '01-Jan-2020'
        users[string_user_id]['blacklist'] = False
        with open(filepath_player_0, 'w') as file:
            json.dump(users, file, indent=4)
        embed = discord.Embed(description='Congratulations, your account has been successfully created.', colour=discord.Color.from_rgb(0,255,133))
        embed.set_author(name='REGISTER', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !daily to claim your first card.')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='Oops, it looks like you already have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !help to see a full list of commands.')
        await ctx.send(embed=embed)



@client.command()
async def daily(ctx):
    string_user_id=str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    if string_user_id in users:
        card_rarity = card_algorithm_1()
        card_name, card_code, card_image = random_card(card_rarity)
        add_card(ctx, card_code)
        if card_rarity == 'rarity1':
            card_rarity = '🃏'
        elif card_rarity == 'rarity2':
            card_rarity = '🃏🃏'
        elif card_rarity == 'rarity3':
            card_rarity = '🃏🃏🃏'
        elif card_rarity == 'rarity4':
            card_rarity = '🃏🃏🃏🃏'
        name_space = ' ' * (25 - len(card_name))
        code_space = ' ' * (25 - len(card_code))
        rarity_space= ' ' * (23 - len(card_rarity * 2))
        embed = discord.Embed(description=f'`NAME: {card_name}{name_space}`\n`RARITY: {card_rarity}{rarity_space}`\n`CODE: {card_code}{code_space}`', colour=discord.Color.from_rgb(0,255,133))
        embed.set_author(name='DAILY', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{card_image}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='Oops, it looks like you don\'t have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !register to create an account.')
        await ctx.send(embed=embed)



@client.command()
async def weekly(ctx):
    string_user_id=str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    if string_user_id in users:
        card_rarity = card_algorithm_2()
        card_name, card_code, card_image = random_card(card_rarity)
        add_card(ctx, card_code)
        if card_rarity == 'rarity1':
            card_rarity = '🃏'
        elif card_rarity == 'rarity2':
            card_rarity = '🃏🃏'
        elif card_rarity == 'rarity3':
            card_rarity = '🃏🃏🃏'
        elif card_rarity == 'rarity4':
            card_rarity = '🃏🃏🃏🃏'
        name_space = ' ' * (25 - len(card_name))
        code_space = ' ' * (25 - len(card_code))
        rarity_space= ' ' * (23 - len(card_rarity * 2))
        embed = discord.Embed(description=f'`NAME: {card_name}{name_space}`\n`RARITY: {card_rarity}{rarity_space}`\n`CODE: {card_code}{code_space}`', colour=discord.Color.from_rgb(0,255,133))
        embed.set_author(name='WEEKLY', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{card_image}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='Oops, it looks like you don\'t have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !register to create an account.')
        await ctx.send(embed=embed)



@client.command()
async def balance(ctx):
    string_user_id = str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    if string_user_id in users:
        balance = users[string_user_id]['currency']
        formatted = ('{:,}').format(balance)
        with open(filepath_player_0, 'w') as file:
            json.dump(users, file, indent=4)
        embed = discord.Embed(description=f'Your current balance is ${formatted}', colour=discord.Color.from_rgb(0,255,133))
        embed.set_author(name='BALANCE', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='Oops, it looks like you don\'t have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !register to create an account.')
        await ctx.send(embed=embed)



@client.command()
async def inventory(ctx):
    string_user_id = str(ctx.author.id)
    with open(filepath_player_0, 'r') as file:
        users = json.load(file)
    if string_user_id in users:
        if users[string_user_id]['cards']:
            embeds = []
            for card in users[string_user_id]['cards']:
                if card[-1] == '1':
                    with open(filepath_rarity_1, 'r') as file:
                        common_file = json.load(file)
                    card_name = common_file['rarity1'][card]['name']
                    card_image = common_file['rarity1'][card]['image']
                    card_code = common_file['rarity1'][card]['code']
                    card_rarity = '🃏'
                elif card[-1] == '2':
                    with open(filepath_rarity_2, 'r') as file:
                        uncommon_file = json.load(file)
                    card_name = uncommon_file['rarity2'][card]['name']
                    card_image = uncommon_file['rarity2'][card]['image']
                    card_code = uncommon_file['rarity2'][card]['code']
                    card_rarity = '🃏🃏'
                elif card[-1] == '3':
                    with open(filepath_rarity_3, 'r') as file:
                        rare_file = json.load(file)
                    card_name = rare_file['rarity3'][card]['name']
                    card_image = rare_file['rarity3'][card]['image']
                    card_code = rare_file['rarity3'][card]['code']
                    card_rarity = '🃏🃏🃏'
                elif card[-1] == '4':
                    with open(filepath_rarity_4, 'r') as file:
                        legendary_file = json.load(file)
                    card_name = legendary_file['rarity4'][card]['name']
                    card_image = legendary_file['rarity4'][card]['image']
                    card_code = legendary_file['rarity4'][card]['code']
                    card_rarity = '🃏🃏🃏🃏'
                name_space = ' ' * (25 - len(card_name))
                code_space = ' ' * (25 - len(card_code))
                rarity_space= ' ' * (23 - len(card_rarity * 2))
                embeds.append(discord.Embed(description=f'`NAME: {card_name}{name_space}`\n`RARITY: {card_rarity}{rarity_space}`\n`CODE: {card_code}{code_space}`\n', colour=discord.Color.from_rgb(0,255,133))
                .set_author(name='INVENTORY', icon_url=f'{ctx.author.avatar_url}')
                .set_image(url=card_image))
            paginator = BotEmbedPaginator(ctx, embeds)
            return await paginator.run()
        else:
            embed = discord.Embed(description=f'Oops, you don\'t seem to have any cards yet.', colour=discord.Color.from_rgb(0,255,133))
            embed.set_author(name='INVENTORY', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text='You can use !daily to claim your first card.') 
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='Oops, it looks like you don\'t have an account.', colour=discord.Color.from_rgb(225,29,98))
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text='You can use !register to create an account.')
        await ctx.send(embed=embed)



###########################################################################################################
###     END                                                                                             ###
###########################################################################################################

client.run(os.getenv('TOKEN_MAIN'))