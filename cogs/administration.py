import discord
from discord.ext import commands
from config import settings

prefix = settings['PREFIX']

class Administration(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def createrole(self, ctx, role):
        role = await ctx.guild.create_role(name = role)
        await ctx.send("Роль сделана!")

    @commands.command()
    async def deleterole(self, ctx, role):
        role = discord.utils.get(ctx.message.guild.roles, name = role)
        await role.delete()
        await ctx.send("Роль удалена!")

    @commands.command()
    async def join(self, ctx):
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def nick(self, ctx, member: discord.Member, *, nick):
        await member.edit(nick = nick)
        await ctx.channel.purge(limit = 1)

async def setup(bot):
    await bot.add_cog(Administration(bot))