import discord
from discord.ext import commands
from config import settings


prefix = settings['PREFIX']

class Information(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(title = 'Команды сервера', colour = discord.Color.red())
        emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.add_field(name = 'Информация', value = f'`{prefix}help` `{prefix}user`', inline = False)
        emb.set_thumbnail(url = ctx.guild.icon)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_roles = True, kick_members = True)
    async def mhelp(self, ctx):
        emb = discord.Embed(title = 'Команды модерации сервера', colour = discord.Color.red())
        emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.add_field(name = '', value = f'`{prefix}mute` `{prefix}unmute` `{prefix}kick` `{prefix}clear`', inline = False )
        emb.set_thumbnail(url = ctx.guild.icon)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ahelp(self, ctx):
        emb = discord.Embed(title = 'Команды администрации сервера', colour = discord.Color.red())
        emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        emb.add_field(name = '', value = f'`{prefix}createrole` `{prefix}deleterole` `{prefix}join` `{prefix}disconnect` `{prefix}nick`', inline = False)
        emb.set_thumbnail(url = ctx.guild.icon)
        await ctx.send(embed = emb)
    

    @commands.command()
    async def user(self, ctx, member: discord.Member = None, guild: discord.Guild = None ):
        if member == None:
            emb = discord.Embed( title = "Основная информация о пользователе", color = ctx.message.author.color )
            emb.add_field( name = "Имя пользователя на данном сервере: ", value = ctx.message.author.display_name, inline = False )
            emb.add_field( name = "Имя пользователя: ", value = ctx.message.author, inline = False )
            emb.add_field( name = "Айди пользователя: ", value = ctx.message.author.id, inline = False )
            status = ctx.message.author.status
            if status == discord.Status.online:
                st = "🟢 В сети"
            status = ctx.message.author.status
            if status == discord.Status.offline:
                st = ":white_circle: Не в сети"
            status = ctx.message.author.status
            if status == discord.Status.idle:
                st = "🌙 Неактивен"
            status = ctx.message.author.status
            if status == discord.Status.dnd:
                st = "⛔ Не беспокоить"
            emb.add_field( name = "Активность: ", value = st, inline = False )
            emb.add_field( name = "Статус: ", value = ctx.message.author.activity, inline = False )
            emb.add_field( name = "Дата регистрации: ", value = ctx.message.author.created_at.strftime( "%d.%m.%Y %H:%M:%S" ), inline = False )
            emb.add_field( name = "Присоединился: ", value = ctx.message.author.joined_at.strftime( "%d.%m.%Y %H:%M:%S" ), inline = False )
            await ctx.send( embed = emb )
        else:
            emb = discord.Embed( title = "Основная информация о пользователе", color = member.color )
            emb.add_field( name = "Имя пользователя на данном сервере: ", value = member.display_name, inline = False )
            emb.add_field( name = "Имя пользователя: ", value = member, inline = False )
            emb.add_field( name = "Айди пользователя: ", value = member.id, inline = False )
            status = member.status
            if status == discord.Status.online:
                st = "🟢 В сети"
            status = member.status
            if status == discord.Status.offline:
                st = ":white_circle: Не в сети"
            status = member.status
            if status == discord.Status.idle:
                st = "🌙 Неактивен"
            status = member.status
            if status == discord.Status.dnd:
                st = "⛔ Не беспокоить"
            emb.add_field( name = "Активность: ", value = st, inline = False )
            emb.add_field( name = "Статус: ", value = member.activity, inline = False )
            emb.add_field( name = "Дата регистрации: ", value = member.created_at.strftime( "%d.%m.%Y %H:%M:%S" ), inline = False )
            emb.add_field( name = "Присоединился: ", value = member.joined_at.strftime( "%d.%m.%Y %H:%M:%S" ), inline = False )
            emb.add_field( name = "Высшая роль на сервере:", value = f"{ member.top_role.mention }", inline = False )
            await ctx.send( embed = emb )

    # @commands.command()
    # async def serverinfo(self, ctx):
    #     guild = ctx.guild
    #     emb = discord.Embed(title = f"Информация о сервере {guild.name}")
    #     emb.add_field(name = "Количество участников:", value = guild.member_count)
    #     emb.add_field(name = "Людей:", value = guild.)
    #     await ctx.send(embed = emb)






    
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
      if member == None:
        author = ctx.author
        emb = discord.Embed(title = f"Аватар {author.display_name}")
        emb.set_image(url = ctx.author.avatar.url)
        await ctx.send(embed = emb)
      else:
        emb = discord.Embed(title = f"Аватар {member.display_name}")
        emb.set_image(url = member.avatar.url)
        await ctx.send(embed = emb)
          
    @commands.command()
    async def time(self, ctx):
        time = "<t:1683878470:f>"
        emb = discord.Embed(title = "Время работы")
        emb.add_field(name = f"Я полноценно работаю с {time}", value = "")
        await ctx.send(embed = emb)


    @mhelp.error
    async def mhelp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'Вы не модератор сервера!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)


    @ahelp.error
    async def ahelp_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title = 'Ошибка!', description = 'Вы не администратор сервера!', colour = discord.Color.red())
            emb.set_author(name = ctx.guild.name)
            await ctx.send(embed = emb)

async def setup(bot):
    await bot.add_cog(Information(bot))