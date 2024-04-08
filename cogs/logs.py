import discord
from discord.ext import commands
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import os

prefix = settings['PREFIX']

# usernamemongo = os.environ['username']
# passwordmongo = os.environ['password']
uri = f"mongodb+srv://moored:daniilmooredb@moore13.9iqj5kj.mongodb.net/?retryWrites=true&w=majority&appName=Moore13"
mongo_client = AsyncIOMotorClient(uri)
db = mongo_client["database"]
system_channel = db["system_channel"]

namecategory = "System Logs"
namechannel = "system-logs"

class Logs(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setuplogs(self, ctx):
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False)
        }
        category = discord.utils.get(guild.categories, name = namecategory)
        channel = discord.utils.get(guild.channels, name = namechannel)
        
        if category is None:
            category = await guild.create_category(name = namecategory, overwrites = overwrites)
        else:
            await ctx.send("Категория уже создана!")
        if channel is None:
            channel = await guild.create_text_channel(name = namechannel, category = category, overwrites = overwrites)
            channel_data = {
                "guild_id": guild.id,
                "channel_id": channel.id
            }
            system_channel.insert_one(channel_data)
        else:
            await ctx.send("Канал уже создан!")
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_data = system_channel.find({"guild_id": member.guild.id})
        async for record in channel_data:
            guild = member.guild
            channel_id = record["channel_id"]
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(f'{member.mention} присоединился к серверу.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_data = system_channel.find({"guild_id": member.guild.id})
        async for record in channel_data:
            guild = member.guild
            channel_id = record["channel_id"]
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(f'{member.mention} покинул сервер.')

    # @commands.Cog.listener()
    # async def on_member_update(self, before, after):
    #     channel_data = system_channel.find({"guild_id": member.guild.id})
    #     async for record in channel_data:
    #         guild = member.guild
    #         channel_id = record["channel_id"]
    #         channel = guild.get_channel(channel_id)
    #         if channel:
    #             await channel.send(f'{member.mention} обновил свой профиль.')
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel_data = system_channel.find({"guild_id": message.guild.id})
        async for record in channel_data:
            guild = message.guild
            channel_id = record["channel_id"]
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(f'{message.author.mention} удалил сообщение: {message.content}')

    # @commands.Cog.listener()
    # async def on_message_edit(self, message, before, after):
    #     channel_data = system_channel.find({"guild_id": message.guild.id})
    #     async for record in channel_data:
    #         guild = message.guild
    #         channel_id = record["channel_id"]
    #         channel = guild.get_channel(channel_id)
    #         if channel:
    #             await channel.send(f'{message.author.mention} отредактировал сообщение: {before.content} -> {after.content}')

    
async def setup(bot):
    await bot.add_cog(Logs(bot))
