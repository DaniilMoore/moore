import discord
from discord.ext import commands
from config import settings


prefix = settings['PREFIX']

class Ticket(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['setc'])
    async def setcategory(self, ctx):
        guild = ctx.guild
        await guild.create_category(name = "Tickets")

    @commands.command()
    async def report(self, ctx):
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages = True, send_messages = False)
        }

        await guild.create_text_channel('question', category = discord.utils.get(guild.channels, name = "Tickets"), overwrites = overwrites)
        
    @commands.command()
    async def setch(self, ctx):
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name = "question")
        emb = discord.Embed(
            title = 'Тикет',
            description = 'Нажмите на  📩 чтобы задать вопрос модерации сервера',
            color = 0
        )
        msg = await channel.send(embed = emb)
        await msg.add_reaction("📩")
        await self.bot.wait_for("reaction_add")


        async def check(self, ctx, reaction, user):

            return user == ctx.author and str(reaction) == '📩'

        stmoder_role = discord.utils.get(guild.roles, name = "st. moder")
        dmainmoder_role = discord.utils.get(guild.roles, name = "deputy main moder") 
        mainmoder_role = discord.utils.get(guild.roles, name = "main moder")

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages = False),
        ctx.author: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = False, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
        stmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
        dmainmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = True, manage_permissions = True, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
        mainmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = True, manage_permissions = True, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
        }

        await guild.create_text_channel(f'ticket - {ctx.author}', category = discord.utils.get(guild.channels, name = "Tickets"), overwrites = overwrites)











    # @commands.command()
    # async def ticket(self, ctx):
        
    #     guild = ctx.guild
    #     embed = discord.Embed(
    #         title = 'Тикет',
    #         description = 'Нажмите на  📩 чтобы задать вопрос модерации сервера',
    #         color = 0
    #     )

    #     msg = await ctx.send(embed=embed)
    #     await msg.add_reaction("📩")
    #     await self.bot.wait_for("reaction_add")

    #     async def check(self, ctx, reaction, user):

    #         return user == ctx.author and str(reaction) == '📩'

    #     #moder_role = discord.utils.get(guild.roles, name = "moder")
    #     stmoder_role = discord.utils.get(guild.roles, name = "st. moder")
    #     dmainmoder_role = discord.utils.get(guild.roles, name = "deputy main moder") 
    #     mainmoder_role = discord.utils.get(guild.roles, name = "main moder")

    #     overwrites = {
    #     guild.default_role: discord.PermissionOverwrite(read_messages = False),
    #     ctx.author: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = False, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
    #     #moder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True ),
    #     stmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
    #     dmainmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = True, manage_permissions = True, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
    #     mainmoder_role: discord.PermissionOverwrite(read_messages = True, create_instant_invite = False, send_messages = True, attach_files = True, mention_everyone = False, change_nickname = True, manage_nicknames = True, manage_channels = True, manage_permissions = True, manage_webhooks = False, send_messages_in_threads = False, create_public_threads = False, create_private_threads = False, add_reactions = True, use_external_emojis = True, use_external_stickers = True, manage_messages = True, manage_threads = False, read_message_history = True, send_tts_messages = False, use_application_commands = True),
    #     }

    #     await guild.create_text_channel(f'ticket - {ctx.author}', category = discord.utils.get(guild.channels, name = "Tickets"), overwrites = overwrites)

async def setup(bot):
    await bot.add_cog(Ticket(bot))