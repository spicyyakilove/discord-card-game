import discord
import random
import sqlite3

from disputils import BotEmbedPaginator
from discord.ext import commands
from lib.functions import *

database = sqlite3.connect('./database/database.sqlite')
cursor = database.cursor()

class inventory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def inventory(self, ctx, user:discord.Member=None):
        if user == None:
            username = str(ctx.author.name)
            userid = int(ctx.author.id)
        else:
            username = str(user.name)
            userid = int(user.id)
        
        cursor.execute(f'SELECT code, game, team, player, teamyear, rarity, issue FROM UserCards WHERE userid={userid} ORDER BY rarity ASC, player ASC, issue ASC;')
        cardlist = cursor.fetchall()
        embeds = []

        desc_title = f'{username} has **{len(cardlist)}** cards in their inventory!'
        if len(cardlist) == 0:
            embed = discord.Embed(description='You don\'t seem to have any cards yet!', colour=discord.Color.from_rgb(255,0,0))
            embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text='You can use !daily to claim your first card.')
            await ctx.send(embed=embed)
        
        else:
            ####################################################################################################
            ## SNOW ⬇️⬇️                                                                                     ##
            ####################################################################################################
            totalpages = (len(cardlist) // 20)
            remainder = len(cardlist) % 20
            for i in range(totalpages):
                desc = ''
                for k in range(20):
                    j = cardlist[(i*20)+k]
                    desc = desc + f'\n` {j[5]}⭐ `—` {j[2]} {j[3]} `—` {j[0]}#{j[6]} `'
                embeds.append(discord.Embed(description=f'{desc_title}\n{desc}', colour=discord.Color.from_rgb(0,0,0))
                .set_author(name='INVENTORY', icon_url=f'{ctx.author.avatar_url}'))
            desc = ''
            for i in range(remainder):
                desc = desc + f'\n` {cardlist[totalpages+i][5]}⭐ `—` {cardlist[totalpages+i][2]} {cardlist[totalpages+i][3]} `—` {cardlist[totalpages+i][0]}#{cardlist[totalpages+i][6]} `'
            embeds.append(discord.Embed(description=f'{desc_title}\n{desc}', colour=discord.Color.from_rgb(0,0,0))
            .set_author(name='INVENTORY', icon_url=f'{ctx.author.avatar_url}'))
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
            ####################################################################################################
            ## SNOW ⬆️⬆️                                                                                     ##
            ####################################################################################################

            # for i in cardlist:
            #     desc = ''
            #     desc = desc + f'\n` {i[5]}⭐ `—` {i[2]} {i[3]} `—` {i[0]}#{i[6]} `'
            #     embeds.append(discord.Embed(description=f'{desc_title}\n{desc}', colour=discord.Color.from_rgb(0,0,0))
            #     .set_author(name='INVENTORY', icon_url=f'{ctx.author.avatar_url}'))
            # paginator = BotEmbedPaginator(ctx, embeds)
            # await paginator.run()

def setup(client):
    client.add_cog(inventory(client))