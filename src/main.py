import discord
import json
import random
from discord.ext import commands
import os
import logging
import datetime
import asyncio

from discord.ext.commands.bot import Bot
from command.PingCommand import PingCommand
from command.RandCommand import RandCommand

def initialiseCommands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))

logging.basicConfig(level=logging.INFO)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './config/json/auth.json')
authF = open(filename,)
TOKEN = json.load(authF)['token']


bot = commands.Bot(command_prefix='£')
bot.ctd_active = False

initialiseCommands(bot)
        
async def ctd(ctx, bot):
    await ctx.send('It be Sunday.')
    while(bot.ctd_active):
        now = datetime.datetime.now()
        day = now.strftime("%A")
        
        #if day == 'Sunday':
        await ctx.send('It be Sunday.')
        
        asyncio.sleep(1)
        
@bot.command(brief='Activates the Boys\' night countdown.', description='Does what it say on the tin.')
async def commence(ctx, *args):
    bot.ctd_active = True
    await ctx.send('The countdown is now inactive.')
    while(bot.ctd_active):
        now = datetime.datetime.now()
        day = now.strftime("%A")
        
        if day == 'Sunday':
            await ctx.send('It be Sunday.')
        
        await asyncio.sleep(1)
    #asyncio.run(ctd(ctx))
    
    
    
    
    
@bot.command(brief='Deactivates the Boys\' night countdown.', description='Does what it say on the tin.')
async def uncommence(ctx, *args):
    bot.ctd_active = False
    await ctx.send('The countdown is now inactive.')

    
bot.run(TOKEN)