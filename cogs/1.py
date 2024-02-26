import discord
from discord.ext import commands
from config import settings
# import youtube_dl
# import asyncio

prefix = settings['PREFIX']

class sda(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

        
#     @commands.command()
#     async def play(self, ctx, url):
#         channel = ctx.message.author.voice.channel
#         vc = await channel.connect()

#         # prepare the music player
#         player = await YTDLSource.from_url(url, loop=self.bot.loop)
#         players[vc.guild.id] = player

#         # start the music player
#         await player.play()

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.2):
#         super().__init__(source, volume)

#         self.requester = data.get('requester')
#         self.title = data.get('title')
#         self.web_url = data.get('webpage_url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({}).extract_info(url, download=False))

#         if 'entries' in data:
#             # take the first item from a playlist
#             data = data['entries'][0]

#         filename = data['url']

#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


        
async def setup(bot):
    await bot.add_cog(sda(bot))