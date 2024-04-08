import discord
from discord.ext import commands
from config import settings
import os
# import keep_alive
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

prefix = settings['PREFIX']
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')
# keep_alive.keep_alive()

# usernamemongo = os.environ['username']
# passwordmongo = os.environ['password']

uri = f"mongodb+srv://moored:daniilmooredb@moore13.9iqj5kj.mongodb.net/?retryWrites=true&w=majority&appName=Moore13"
mongo_client = AsyncIOMotorClient(uri)
db = mongo_client["database"]

async def ensure_server_collection(server_id):
    if str(server_id) not in await db.list_collection_names():
        await db.create_collection(str(server_id))
    
class ServerSettings:
    def __init__(self, server_id):
        self.server_id = server_id

    @property
    def collection(self):
        return db[str(self.server_id)]

@client.command()
async def save(ctx, *, message):
    server_settings = ServerSettings(ctx.guild.id)
    collection = server_settings.collection
    await collection.insert_one({"author": ctx.author.id, "content": message})
    await ctx.send("Сообщение сохранено!")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit = 1)

async def get_messages_by_author(server_id, author_id):
    server_settings = ServerSettings(server_id)
    collection = server_settings.collection
    messages = await collection.find({"author": author_id}).to_list(length=None)
    return messages

@client.command()
async def get_messages(ctx, author_id):
    messages = await get_messages_by_author(ctx.guild.id, int(author_id))
    if messages:
        await ctx.send(f"Сообщения пользователя {author_id}:")
        for message in messages:
            await ctx.send(f"Содержание: {message['content']}")
    else:
        await ctx.send("Сообщений от данного пользователя не найдено.")
    
@client.event
async def on_ready():
    print(f"Logged on as {settings['NAME BOT']}")
    await client.tree.sync()

    for guild in client.guilds:
        await ensure_server_collection(guild.id)
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')

    # for i in client.guilds:
    #     inv = await i.text_channels[0].create_invite(max_age=0, max_uses=100, temporary=False)
    #     print(inv)
    
@client.tree.command(name="slash",description="this is test slash command")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("test")
    
@client.tree.command(name="ping", description="ping")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {bot_latency} ms.")

my_secret = "OTU5NDQwMjkyNjQ4NDcyNjM4.G_TvF5.R8FgAK4RgSePvN93RoTNydwSNeHa1DCBVe63V0"
client.run(my_secret)
