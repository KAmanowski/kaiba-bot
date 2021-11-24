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
    
    SERVER = "kaiba"
    CHANNEL = "bantercave"
    
    def __init__(self, bot):
        super().__init__()
        self.bot: Bot = bot
        
    async def send_message(self, message: str):
        channel = self.bot.get_channel(ConfigReader.get_channel_id(self.SERVER, self.CHANNEL))
        isinstance(channel, TextChannel)
        
        await channel.send(message)
        
    @commands.command()
    async def book(self, ctx: Context, *args):
        self.bot: Bot
        
        if len(args) != 3:
            await ctx.send('Wrong number of arguments.')
            return
            
        givenUserId = args[1]
        try:
            int(args[1])
        except:
            try:
                givenUserId = str(args[1])[3:-1]
                int(givenUserId)
            except:
                await ctx.send('I need a valid user Id.')
                return
            
        if args[0] == 'yellow' or args[0] == 'red':      
            try:
                user: User = await self.bot.fetch_user(givenUserId)
                # User booking entry
                booking = Booking(args[2], ctx.message.author.id, datetime.now().timestamp())
                # Booking entry from Kaiba Bot
                kaibaBooking = Booking("Two new yellow cards.", self.bot.id, datetime.now().timestamp())
                
                if args[0] == 'yellow':
                    DynamicConfigWriter.command_book('yellow', user.id, booking)
                    await self.send_message(f"<@!{user.id}> has been given a yellow card by <@!{ctx.message.author.id}>. Reason: '{args[2]}'")
                    
                    yellowBookings = DynamicConfigReader.command_get_bookings('yellow', user.id)
                    redBookings = DynamicConfigReader.command_get_bookings('red', user.id)
                    # If there is more than two yellow cards
                    if len(yellowBookings) >= 2:
                        # If its a multiple of two (2, 4, 6 etc.) then it's time for a red card
                        if len(yellowBookings) % 2 == 0:
                            if len(redBookings) > 0:
                                await self.send_message(f"Oh wow <@!{user.id}>, another red card in one week. I wouldn't wanna be you come friday.")
                            else:
                                await self.send_message(f"<@!{user.id}>, you now have a red card. Prepare for friday.")
                            DynamicConfigWriter.command_book('red', user.id, kaibaBooking)
                else:
                    await self.send_message(f"Woah, you've pissed someone off <@!{user.id}>. You've been given a red card by <@!{ctx.message.author.id}>. Reason: '{args[2]}'")
                    DynamicConfigWriter.command_book('red', user.id, booking)

            except NotFound:
                await ctx.send(f'Cannot find user {args[0]}')
        else:
            await ctx.send('Card can only be yellow or red.')