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
            code, game, team, player, issue, image = select_random_card(rarity)
            insert_card(code, game, team, player, rarity, issue, userid)
            balance = select_balance_rarity()
            add_balance(balance, userid)
            embed = discord.Embed(description=f'`GAME: {game}`\n`TEAM: {team}`\n`PLAYER: {player}`\n`RARITY: {rarity}`\n`ISSUE: {issue+1}`\n`CODE: {code}`\n \n`BAL: +{balance}`', colour=discord.Color.from_rgb(0,255,133))
            embed.set_author(name='WEEKLY', icon_url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(weekly(client))