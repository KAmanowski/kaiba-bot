from datetime import datetime, time
from discord.abc import User
from discord.channel import TextChannel
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from domain.Booking import Booking
from util.ConfigReader import ConfigReader

from util.DynamicConfigReader import DynamicConfigReader
from util.DynamicConfigWriter import DynamicConfigWriter

class BookCommand(commands.Cog):
    "£book allows you to book someone with a yellow or red card."
    
    SERVER = "kaiba"
    CHANNEL = "bantercave"
    
    help_brief = "Allows you to book someone with a yellow or red card."
    help_description = "To book someone you need to choose a card (yellow/red), their userId (can just @) and a reason in quotes (\"Cause they stink.\")."
    
    def __init__(self, bot):
        super().__init__()
        self.bot: Bot = bot
        
    async def send_message(self, message: str):
        channel = self.bot.get_channel(ConfigReader.get_channel_id(self.SERVER, self.CHANNEL))
        isinstance(channel, TextChannel)
        
        await channel.send(message)
        
    @commands.command(name="book", brief=help_brief, description=help_description)
    async def book(self, ctx: Context, card, userId, reason):
        self.bot: Bot
            
        givenUserId = userId
        try:
            int(userId)
        except:
            try:
                givenUserId = str(userId)[3:-1]
                int(givenUserId)
            except:
                await ctx.send('I need a valid user Id.')
                return
            
        if card == 'yellow' or card == 'red':      
            try:
                user: User = await self.bot.fetch_user(givenUserId)
                # User booking entry
                booking = Booking(reason, ctx.message.author.id, datetime.now().timestamp())
                # Booking entry from Kaiba Bot
                kaibaBooking = Booking("Two new yellow cards.", self.bot.id, datetime.now().timestamp())
                
                if card == 'yellow':
                    DynamicConfigWriter.command_book('yellow', user.id, booking)
                    await self.send_message(f"<@!{user.id}> has been given a yellow card by <@!{ctx.message.author.id}>. Reason: '{reason}'")
                    
                    yellowBookings = DynamicConfigReader.command_get_bookings('yellow', user.id)
                    redBookings = DynamicConfigReader.command_get_bookings('red', user.id)
                    # If there is more than two yellow cards
                    if len(yellowBookings) % 2 == 0:
                        if len(redBookings) > 0:
                            await self.send_message(f"Oh wow <@!{user.id}>, another red card in one week. I wouldn't wanna be you come friday.")
                        else:
                            await self.send_message(f"<@!{user.id}>, you now have a red card. Prepare for friday.")
                        DynamicConfigWriter.command_book('red', user.id, kaibaBooking)
                else:
                    await self.send_message(f"Woah, you've pissed someone off <@!{user.id}>. You've been given a red card by <@!{ctx.message.author.id}>. Reason: '{reason}'")
                    DynamicConfigWriter.command_book('red', user.id, booking)

            except NotFound:
                await ctx.send(f'Cannot find user {card}')
        else:
            await ctx.send('Card can only be yellow or red.')