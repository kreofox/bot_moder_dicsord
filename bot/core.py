import os 

import discord
import youtube_dl
from discord.ext import commands

from config import PREFIX, SEND_PUNISHMENT_PERSONAL_MESSAGE, TOKEN, DELETE_COMMANDS, MUTE_ROLE_ID, E_CHAT_FILTRATION,BAD_WORD_LIST,USE_CHAT_FILTRATION

import requests
from PIL import Image,ImageFont,ImageDraw
import io

#Настроика префикса для команд 
client=commands.Bot(command_prefix='PREFIX')
client.remove_command('help')


def main():
    @client.event
    async def on_connet():
        """Сообщение при подключении"""
        print('бот подключен')
        await client.change_presence(status=discord.Status.online,activity=discord.Game(f'{PREFIX}help'))

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{ctx.author.mention}, такой команды не существует, воспользуйтесь справкой, введя {PREFIX}help')
        else:
            print(error)

    @client.event
    async def on_message(message: discord.Message):
        if USE_CHAT_FILTRATION:
            await client.process_commands(message)
            msg = message.content.lower()
        if msg in BAD_WORD_LIST:
            await message.delete()
            await message.channel.send(f'{message.author.mention},не надо так писать!')
    
    @client.command(name="help")
    async def _help(ctx):
        """Справка по командам"""
        if DELETE_COMMANDS:
            await ctx.message.delete()
        embed = discord.Embed(title='Cправка по командам',
                                  description=f'Все команды у этого бота начинаются с "{PREFIX}"',
                                  color=discord.Color.orange()) 
        embed.set_author(name=client.user.name,icon_url=client.user.avatar_url)
        embed.add_field(name=f'{PREFIX}help', value='Выводит команды')
        embed.add_field(name=f'{PREFIX}kick ПОЛЬЗОВАТЕЛЬ')
        embed.add_field(name=f'{PREFIX}ban ПОЛЬЗОВАТЕЛЯ',
                            value='Навсегда блокрует участника пользователя на сервере по причине.')
        embed.add_field(name=f'{PREFIX}unban ID_ПОЛЬЗОВАТЕЛЯ',
                        value='Разблокирует участника с ID ID_ПОЛЬЗОВАТЕЛЯ на сервере, если он был заблокирован.')
        embed.add_field(name=f'{PREFIX}mute ПОЛЬЗОВАТЕЛЬ',
                        value='Навсегда запрещает участнику ПОЛЬЗОВАТЕЛЬ писать сообщения в текстовых каналах.')
        embed.add_field(name=f'{PREFIX}unmute ПОЛЬЗОВАТЕЛЬ',
                        value='Разрешает участнику ПОЛЬЗОВАТЕЛЬ писать сообщения в текстовые каналы, если до этого он '
                              'не мог это делать.')
        embed.add_field(name=f'{PREFIX}join',
                        value='Бот присоединится к голосовому каналу пользователя, вызвавшего команду.')
        embed.add_field(name=f'{PREFIX}leave', value='Бот покинет голосовой канал.')
        embed.add_field(name=f'{PREFIX}play YOUTUBE_ССЫЛКА', value='Играет аудио по ссылке YOUTUBE_ССЫЛКА.')
        embed.add_field(name=f'{PREFIX}card', value='Показывает карточку пользователя.')
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @client.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def _kick(ctx, member: discord.Member, *, reason: str = None):
        """Кикнуть участника"""
        if DELETE_COMMANDS:
            await ctx.message.delete()
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f'Участник {member.mention} выгнан с сервера.\nПричина: "{reason}".')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await member.send(f'Вы были выгнаны с сервера по причине: "{reason}".')
        else:
            await ctx.send(f'Участник {member.mention} выгнан с сервера без причины.')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await member.send('Вы были выгнаны с сервера без причины.')
    
    @client.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def _ban(ctx, member: discord.Member, *, reason: str = None):
        """Забанить участника"""
        if DELETE_COMMANDS:
            await ctx.message.delete()
        await member.ban(reason=reason)
        if reason:
            await ctx.send(f'Участник {member.mention} забанен на сервере.\nПричина: "{reason}".')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await member.send(f'Вы были забанены на сервере по причине: "{reason}".')
        else:
            await ctx.send(f'Участник {member.mention} забанен на сервере без причины.')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await member.send('Вы были забанены на сервере без причины.')

    @client.command(name='unban')
    @commands.has_permissions(administrator=True)
    async def _unban(ctx, *, user_id: int):
        """Разбанить участника"""
        await ctx.message.delete()
        try:
            user = await client.fetch_user(user_id=user_id)
            await ctx.guild.unban(user)
            await ctx.send(f'Участник с ID {user_id} успешно разбанен.')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await user.send('Вы были разбанены на сервере.')
        except discord.DiscordException:
            await ctx.send(f'Участник с ID {user_id} не забанен, поэтому не может быть разбанен.')
     
    @client.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def _mute(ctx, member: discord.Member):
        """Замьютить участника"""
        if DELETE_COMMANDS:
            await ctx.message.delete()
        mute_role = discord.utils.get(ctx.message.guild.roles, id=MUTE_ROLE_ID)
        await member.add_roles(mute_role)
        await ctx.send(f'Участник {member.mention} теперь может только читать сообщения.')
        if SEND_PUNISHMENT_PERSONAL_MESSAGE:
            await member.send('Вы были замьючены на сервере.')

    @client.command(name='unmute')
    @commands.has_permissions(administrator=True)
    async def _unmute(ctx, member: discord.Member):
        """Размьютить участника"""
        if DELETE_COMMANDS:
            await ctx.message.delete()
        mute_role = discord.utils.get(ctx.message.guild.roles, id=MUTE_ROLE_ID)
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'Участник {member.mention} снова может писать в чат.')
            if SEND_PUNISHMENT_PERSONAL_MESSAGE:
                await member.send('Вы были размьючены на сервере.')
        else:
            await ctx.send(f'Участник {member.mention} не в мьюте, поэтому не может быть размьючен.')

    @client.command(name='join')
    async def _join(ctx):
        """Присоединится в голосовой канал"""
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f'Бот присоединился к каналу {channel}')

    @client.command(name='leave')
    async def _leave(ctx):
        """Покинуть голосовой канал"""
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Бот отключился от канала {channel}')
        else:
            await ctx.send('Бот не подключен к голосовому каналу и не может быть отключен.')

    @client.command(name='play')
    async def _play(ctx, url: str):
        """Воспроизведение музыки"""
        song_there = os.path.isfile("tmp/song.mp3")
        try:
            if song_there:
                os.remove("tmp/song.mp3")
        except PermissionError:
            return
        await ctx.send("Ожидайте...")
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'outtmpl': os.path.abspath('tmp') + '/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./tmp"):
            os.chdir('./tmp')
            if file.endswith(".mp3"):
                name = file
                os.rename(file, "song.mp3")
            os.chdir('../')
        if voice is None:
            voice = await ctx.message.author.voice.channel.connect()
        os.chdir('./tmp')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        os.chdir('../')
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await ctx.send(f"Играет: {name}.")

    @client.command(name='card')
    async def _card(ctx):
        img = Image.new('RGBA', (400, 200), '#FD7C00')
        url = str(ctx.author.avatar_url)[:-10]
        response = requests.get(url, stream=True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)
        img.paste(response, (15, 15, 115, 115))
        idraw = ImageDraw.Draw(img)
        name = ctx.author.name
        tag = ctx.author.discriminator
        headline = ImageFont.truetype('fonts/russo_one.ttf', size=20)
        undertext = ImageFont.truetype('fonts/russo_one.ttf', size=12)
        idraw.text((145, 15), f'{name}#{tag}', font=headline)
        idraw.text((145, 50), f'ID: {ctx.author.id}', font=undertext)
        img.save('user_card.png')
        await ctx.send(file=discord.File(fp='user_card.png'))

    @_kick.error
    @_ban.error
    @_unban.error
    @_mute.error
    @_unmute.error
    async def moderation_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.author.mention}, вы неверно ввели аргументы, воспользуйтесь командой {PREFIX}help для справки.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у вас недостаточно прав для выполнения данной команды.')

    # Запуск бота
    client.run(TOKEN)
 