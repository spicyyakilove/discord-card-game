import discord
import random
import sqlite3

from discord.ext import commands
from lib.functions import *

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

class inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def inventory(self, ctx):
        userid = int(ctx.author.id)
        cursor.execute(f'SELECT code, game, team, player, teamyear, rarity, issue FROM UserCards WHERE userid={userid} ORDER BY rarity ASC, team ASC, player ASC, issue ASC LIMIT 20;')
        cardlist = cursor.fetchall()
        if len(cardlist) == 0:
            embed = discord.Embed(description='You don\'t seem to have any cards yet!', colour=discord.Color.from_rgb(255,0,0))
            embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text='You can use !help to see a full list of commands.')
            await ctx.send(embed=embed)
        else:
            desc = ''
            for i in cardlist:
                desc = desc + f'\n` {i[5]}⭐ `—` {i[2]} `—` {i[3]} `—` {i[0]}#{i[6]} `'
            embed = discord.Embed(description=f'{desc}', colour=discord.Color.from_rgb(0,0,0))
            embed.set_author(name=f'INVENTORY', icon_url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(inventory(client))