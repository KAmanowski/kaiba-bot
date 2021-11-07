import discord
import json
import random
from discord.ext import commands
import os
import logging
import datetime
import asyncio

logging.basicConfig(level=logging.INFO)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../auth.json')
authF = open(filename,)
TOKEN = json.load(authF)['token']


bot = commands.Bot(command_prefix='£')
bot.ctd_active = False

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# WORKS
@bot.command(brief='Gives you a random number.', description='[£rand n] will give a number from 0 to n, [£rand n m] will give a number from n to m.')
async def rand(ctx, *args):
    argLen = len(args)
    
    validArgs = True
    
    for i in args:
        try:
            int(i)
        except ValueError:
            await ctx.send("One of your arguments isn't a number you fucking idiot.")
            validArgs = False
            
    if (validArgs):
        if (argLen == 0):  
            await ctx.send(str(random.random()))
        elif (argLen == 1):
            await ctx.send(str(random.randint(0, int(args[0]))))
        else:
            await ctx.send(str(random.randint(int(args[0]), int(args[1]))))
        
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