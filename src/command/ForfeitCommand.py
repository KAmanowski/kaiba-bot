from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigReader import DynamicConfigReader
from util.DynamicConfigWriter import DynamicConfigWriter

class ForfeitCommand(commands.Cog):
    "£forfeit allows you to manage forfeits for red card recipients."
    
    help_brief = "Using the forfeit command you can add/delete forfeits and also see them all in a big list."
    help_description = "Forfeits are "
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    def generate_list_message(self, forfeits: list) -> str:
        out = "```"
        out += "All the available forfeits:\n\n"
        forfeitId = 0
        
        for forfeit in forfeits:
            out += f"{forfeitId}: {forfeit}\n\n"
            forfeitId += 1
        
        out += "```"
        return out
            
    def remove_forfeits(self, forfeits: list, idsToRemove: list) -> list:
        dictForfeits = {}
        
        # Add all forfeits to dictionary keyed by id
        for i in range(len(forfeits)):
            dictForfeits[f'{i}'] = forfeits[i]
        
        forfeits = []
        # Create new list using only ids that arent deleted
        for i in dictForfeits.keys():
            if not (i in idsToRemove):
                forfeits.append(dictForfeits[i])
        
        return forfeits    
        
        
    @commands.command(name="forfeit", brief=help_brief, description=help_description)
    async def forfeit(self, ctx: Context, function, *, forfeitOrIds=""):
        forfeits = DynamicConfigReader.command_get_forfeits()
        
        match function:
            case 'list':
                await ctx.send(self.generate_list_message(forfeits))
            case 'add':
                forfeits.append(forfeitOrIds)
                DynamicConfigWriter.command_write_forfeits(forfeits)
                await ctx.send(f"Added forfeit: {forfeitOrIds}")
            case 'remove':
                idsToRemove = forfeitOrIds.split(" ")
                try:
                    for _id in idsToRemove:
                        int(_id)
                except:
                    await ctx.send("Give a list of valid Ids separated by space.")
                    return
                
                DynamicConfigWriter.command_write_forfeits(self.remove_forfeits(forfeits, idsToRemove))
                await ctx.send('Removed requested forfeits.')
            case _:
                await ctx.send(f"No such function: {function}")