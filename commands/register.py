import discord
import datetime
import random
import sqlite3

from discord.ext import commands
from lib.functions import *

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

class register(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def register(self, ctx):
        userid = int(ctx.author.id)
        registered = check_users_exists(userid)
        if registered != None:
            embed = discord.Embed(description='You already have an account. Get playing!', colour=discord.Color.from_rgb(255,0,0))
            embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text='You can use !help to see a full list of commands.')
            await ctx.send(embed=embed)
        else:
            blacklist = 0
            currency = 500
            date = datetime.datetime.now().date()
            query = f"INSERT INTO Users VALUES ({int(userid)}, {int(blacklist)}, {int(currency)}, '{str(date)}');"
            cursor.execute(query); database.commit()
            embed = discord.Embed(description='Congratulations, your account has been successfully created.\n', colour=discord.Color.from_rgb(0,0,0))
            embed.set_author(name='REGISTER', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text='You can use !daily to claim your first card.')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(register(client))