import discord
import random
import sqlite3

from discord.ext import commands
from lib.functions import *

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

class weekly(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def weekly(self, ctx):
        userid = int(ctx.author.id)
        rarity = select_card_rarity()
        while rarity == '1':
            rarity = select_card_rarity()
        else:
            code, game, team, player, issue, teamyear, image = select_random_card(rarity)
            insert_card(game, team, player, rarity, issue, teamyear, code, userid, image)
            balance = select_balance_rarity()
            add_balance(balance, userid)
            issue_str = str(issue)
            bal_str = str(balance)
            g_space = ' ' * (31 - len(game))
            t_space = ' ' * (31 - len(team))
            p_space = ' ' * (31 - len(player))
            c_space = ' ' * (30 - (len(code) + len(issue_str)))
            b_space = ' ' * (24 - len(bal_str))
            embed = discord.Embed(description=f'`{game}{g_space}`\n`{team}{t_space}`\n`{player}{p_space}`\n`{code}#{issue+1}{c_space}`\n`+{balance} Coins{b_space}`', colour=discord.Color.from_rgb(0,0,0))
            embed.set_author(name='WEEKLY', icon_url=f'{ctx.author.avatar_url}')
            embed.set_image(url=f'{image}')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(weekly(client))