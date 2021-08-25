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
        registered = check_users_exists(userid)
        if registered == None:
            await ctx.send(embed=account_embed(ctx))
        else:
            blacklisted = check_if_blacklisted(userid)
            if blacklisted == 1:
                await ctx.send(embed=blacklist_embed(ctx))
            else:
                rarity = select_card_rarity()
                code, game, team, player, issue, teamyear, image = select_random_card(rarity)
                insert_card(game, team, player, rarity, issue, teamyear, code, userid, image)
                issue1 = issue + 1
                issue_str = str(issue1)
                g_space = ' ' * (31 - len(game))
                t_space = ' ' * (31 - len(team))
                p_space = ' ' * (31 - len(player))
                c_space = ' ' * (30 - (len(code) + len(issue_str)))
                embed = discord.Embed(description=f'`{game}{g_space}`\n`{team}{t_space}`\n`{player}{p_space}`\n`{code}#{issue1}{c_space}`', colour=discord.Color.from_rgb(0,0,0))
                embed.set_author(name='DAILY', icon_url=f'{ctx.author.avatar_url}')
                embed.set_image(url=f'{image}')
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(daily(client))