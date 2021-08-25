import discord
import dotenv
import sqlite3
import os

from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)
database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()
load_dotenv()

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def deactivate(ctx, command=None):
    if command == None:
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                client.unload_extension(f'commands.{filename[:-3]}')
        await ctx.send(f'`All commands have been deactivated.`')
    else:
        client.unload_extension(f'commands.{command}')
        await ctx.send(f'`{command.capitalize()} has been deactivated.`')

@client.command()
@commands.is_owner()
async def activate(ctx, command=None):
    if command == None:
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                client.load_extension(f'commands.{filename[:-3]}')
        await ctx.send(f'`All commands have been activated.`')
    else:
        client.load_extension(f'commands.{command}')
        await ctx.send(f'`{command.capitalize()} has been activated.`')

client.run(os.getenv('TOKEN_MAIN'))