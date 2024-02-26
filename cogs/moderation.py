import discord
from discord.ext import commands
import asyncio
from config import settings
from discord import app_commands
from datetime import datetime

prefix = settings['PREFIX']

class Moderation(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member: discord.Member, time: int, *, reason):
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title = 'Мут текстового чата', description = f'Пользователь {member.mention} получил мут на {time} минут(-у)(-ы) по причине: {reason}', colour = discord.Color.red())
        emb.set_author(name = ctx.guild.name)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.set_thumbnail(url = member.avatar.url)
        await ctx.send(embed = emb)
        muted_role = discord.utils.get(ctx.message.guild.roles, name = "Mute")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name = "Mute")
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(muted_role, send_messages = False)
        await member.add_roles(muted_role)
        await asyncio.sleep(time * 60)
        await member.remove_roles(muted_role)

    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def vmute(self, ctx, member: discord.Member, time: int, *, reason):
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title = 'Мут голосового чата', description = f'Пользователь {member.mention} получил мут голосового чата на {time} минут(-у)(-ы) по причине: {reason}', colour = discord.Color.red())
        emb.set_author(name = ctx.guild.name)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.set_thumbnail(url = member.avatar.url)
        await ctx.send(embed = emb)
        vmuted_role = discord.utils.get(ctx.message.guild.roles, name = "Voice Mute")
        if not vmuted_role:
            vmuted_role = await ctx.guild.create_role(name = "Voice Mute")
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(vmuted_role, speak = False)
        await member.add_roles(vmuted_role)
        await member.move_to(None)
        await asyncio.sleep(time * 60)
        await member.remove_roles(vmuted_role)
        await member.move_to(None)

    @commands.command()
    @commands.has_permissions(moderate_members = True)
    async def unvmute(self, ctx, member: discord.Member):
        vmuted_role = discord.utils.get(ctx.message.guild.roles, name = "Voice Mute")
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title = 'Размут голосового чата', description = f'С пользователя {member.mention} был снял мут голосового чата.', colour = discord.Color.red())
        emb.set_author(name = ctx.guild.name)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.set_thumbnail(url = member.avatar.url)
        await ctx.send(embed = emb)
        await member.remove_roles(vmuted_role)
    
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.message.guild.roles, name = "Mute")
        await ctx.message.add_reaction('✅')
        emb = discord.Embed(title = 'Размут текстового чата', description = f'С пользователя {member.mention} был снял мут.', colour = discord.Color.red())
        emb.set_author(name = ctx.guild.name)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.set_thumbnail(url = member.avatar.url)
        await ctx.send(embed = emb)
        await member.remove_roles(muted_role)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, reason):
        await ctx.message.add_reaction('✅')
        await member.kick(reason = reason)
        emb = discord.Embed(title = 'Кик', description = f'Пользователь {member.mention} был кикнут по причине: {reason}', colour = discord.Color.red())
        emb.set_author(name = ctx.guild.name)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.set_thumbnail(url = member.avatar.url )
        await ctx.send(embed = emb)
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 100):
        await ctx.channel.purge(limit = amount + 1)
        emb = discord.Embed(title = 'Очистка сообщений', description = f'Было удалено {amount} сообщений(-е)(-я)!')
        await ctx.send(embed = emb)
        await asyncio.sleep(3)
        await ctx.channel.purge(limit = 1)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument ):
            emb = discord.Embed(title = f'Команда `{prefix}kick`', description = 'Кикает участника с сервера.', colour = discord.Color.red() )
            emb.set_author(name = ctx.guild.name)
            emb.add_field(name = 'Использование:', value = "`!kick @<Участник/ID> Причина: `", inline = False )
            emb.add_field(name = 'Пример:', value = "`!kick @Участник#1234 нарушение правил сервера`\n┗ Кикнет указанного участника с причиной 'нарушение правил сервера' ", inline = False )
            await ctx.send (embed = emb )
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'У вас недостаточно прав!', colour = discord.Color.red() )
            emb.set_author(name = ctx.guild.name)
            await ctx.send (embed = emb)
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(title = f'Команда `{prefix}mute`', description = 'Выдаёт мут участника в тектовом чате на определённое время.', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            emb.add_field(name = 'Использование:', value = '`!mute @<Участник/ID> Время(в минутах), Причина`', inline = False)
            emb.add_field(name = 'Пример:', value = "`!mute @Участник#1234 10 нарушение правил сервера`\n┗Замутит указанного участника в текстовом чате с причиной 'нарушение правил сервера' на 10 минут.", inline = False)
            await ctx.send(embed = emb)
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'У вас недостаточно прав!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(title = f'Команда `{prefix}unmute`', description = 'Снимает мут текстового чата.', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            emb.add_field(name = 'Использование:', value = '`!unmute @<Участник/ID>`', inline = False)
            emb.add_field(name = 'Пример:', value = "`!unmute @Участник#1234`\n┗Снимет мут текстового чата у указанного пользователя.", inline = False)
            await ctx.send(embed = emb)
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'У вас недостаточно прав!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)

    @vmute.error
    async def vmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(title = f'Команда `{prefix}vmute`', description = 'Выдаёт мут голосового канала участнику.')
            emb.set_author(name = ctx.guild.name)
            emb.add_field(name = 'Использование:', value = '`!vmute @<Участник/ID> Время(в минутах), Причина`', inline = False)
            emb.add_field(name = 'Пример:', value = "`!vmute @Участник#1234 10 нарушение правил сервера`\n┗Замутит указанного участника в голосовом канала с причиной 'нарушение правил сервера' на 10 минут.", inline = False)
            await ctx.send(embed = emb)
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'У вас недостаточно прав!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)

    @unvmute.error
    async def unvmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(title = f'Команда `{prefix}unvmute`', description = 'Снимает мут голосового канала у участника.', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            emb.add_field(name = 'Использование:', value = '`!unvmute @<Участник/ID>`', inline = False)
            emb.add_field(name = 'Пример:', value = "`!unvmute @Участник#1234`\n┗Снимет мут голосового канала у указанного пользователя.", inline = False)
            await ctx.send(embed = emb)
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description ='У вас недостаточно прав!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'У вас недостаточно прав!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)
    
    
    @app_commands.command()
    @app_commands.checks.has_permissions(moderate_members = True)
    async def timeoute(self, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
        await member.timeoute(duration, reason=reason)


async def setup(bot):
    await bot.add_cog(Moderation(bot))