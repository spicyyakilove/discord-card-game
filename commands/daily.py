import discord
import random
import sqlite3

from discord.ext import commands
from lib.functions import *

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

class daily(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def daily(self, ctx):
        userid = int(ctx.author.id)
        rarity = select_card_rarity()
        code, game, team, player, issue, image = select_random_card(rarity)
        insert_card(code, game, team, player, rarity, issue, userid)
        issue_str = str(issue)
        g_space = ' ' * (31 - len(game))
        t_space = ' ' * (31 - len(team))
        p_space = ' ' * (31 - len(player))
        c_space = ' ' * (30 - (len(code) + len(issue_str)))
        embed = discord.Embed(description=f'`{game}{g_space}`\n`{team}{t_space}`\n`{player}{p_space}`\n`{code}#{issue+1}{c_space}`', colour=discord.Color.from_rgb(0,0,0))
        embed.set_author(name='DAILY', icon_url=f'{ctx.author.avatar_url}')
        embed.set_image(url=f'{image}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(daily(client))