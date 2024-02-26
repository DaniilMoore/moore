import discord
from discord.ext import commands
from config import settings

prefix = settings['PREFIX']

class Logs(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
    
        return

async def setup(bot):
    await bot.add_cog(Logs(bot))