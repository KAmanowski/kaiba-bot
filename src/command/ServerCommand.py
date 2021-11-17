from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from exception.BadInputException import BadInputException
from exception.MerlinErrorException import MerlinErrorException

from provider.Merlin import Merlin
from util.DynamicConfigReader import DynamicConfigReader
from util.DynamicConfigWriter import DynamicConfigWriter

class ServerCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.lock = False
        
    async def start_server(self, ctx: Context, server: str):
      self.message = await ctx.send('Attempting to start server ' + str.upper(server) + '.')
      Merlin.server_command(server, 'start')
      await self.message.edit(content='<:coolio:802363745170358282> Server ' + str.upper(server) + ' has been started - just give it a couple of seconds to set up.')
    
    async def kill_server(self, ctx: Context, server: str):
      self.message = await ctx.send('Attempting to kill server ' + str.upper(server) + '.')
      Merlin.server_command(server, 'kill')
      await self.message.edit(content='<:pain:797622064701636648> Server ' + str.upper(server) + ' has been killed')
    
    async def restart_server(self, ctx: Context, server: str):
      self.message = await ctx.send('Attempting to restart server ' + str.upper(server) + '.')
      Merlin.server_command(server, 'restart')
      await self.message.edit(content='<:nut:802365320458403861> Server ' + str.upper(server) + ' has been restarted')
        
    @commands.command()
    async def server(self, ctx: Context, *args):
      self.message: Message = None
      if self.lock == False:
        try:
          if len(args) == 2:
            # Lock command
            self.lock = True
            
            command = str.lower(args[0])
            server = str.lower(args[1])
            match command:
              case 'start':
                await self.start_server(ctx, server)
              case 'kill':
                await self.kill_server(ctx, server)
              case 'restart':
                await self.restart_server(ctx, server)
              case _:
                await ctx.send(command + ' is not a valid command.')
        
        except BadInputException as e:
          await self.message.edit(content="Merlin says you fucked up: '" + str(e) + "'")
          await ctx.send('<:disgust2:906313723147354173>')
        except MerlinErrorException:
          await self.message.edit(content='Merlin is offline/has died. Try again, maybe it might work.')
        except:
          await self.message.edit(content='Alright, not even I know what went wrong. No server command for you.')
        
        # Unlock command
        self.lock = False
      else:
        await ctx.send('There is already a server command running, chill. Stop trying to break my ass.')