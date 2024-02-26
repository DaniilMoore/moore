import discord
from discord.ext import commands
from config import settings
import os
import keep_alive
from discord import app_commands

prefix = settings['PREFIX']
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')
keep_alive.keep_alive()


@client.event
async def on_ready():
    print(f"Logged on as {settings['NAME BOT']}")
    await client.tree.sync()

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')

            
@client.tree.command(name="slash",description="this is test slash command")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("test")
    
my_secret = os.environ['TOKEN']
client.run(my_secret)