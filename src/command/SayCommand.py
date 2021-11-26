from discord import User, Member
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
import asyncio
import time
class SayCommand(commands.Cog):
    "£say makes the bot say something in your current voice channel."
    
    help_brief = "If you need the bot to say something in your voice channel - tell 'im."
    help_description = "Simple ping - the bot will respond with 'pong'."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="say", brief=help_brief, description=help_description)
    async def say(self, ctx: Context):
        user: Member = ctx.message.author
        voice_channel = user.voice
        vc = None
        try:
            await voice_channel.channel.connect()
            vc = ctx.voice_client
        except:
            vc = ctx.voice_client
            pass
        
        if not vc:
            await ctx.send('You need to be in a voice channel on the server you are calling this from.')
        
        try:
            # Lets play that mp3 file in the voice channel
            vc.play(discord.FFmpegPCMAudio("D:\Documents\Projects\git\kaiba-bot\src\clips\\forbidden-word.mp3"), after=lambda e: print(f"Finished playing: {e}"))

            # Lets set the volume to 1
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1

        # Handle the exceptions that can occur
        except:
            raise