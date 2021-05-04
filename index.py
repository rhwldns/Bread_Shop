from discord.ext import commands
from discord.ext import tasks
import discord
import os
from os import popen
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['bs.', 'bs. '], help_command=None, intents=intents)

extensions = ['cogs.Send']

if __name__ == "__main__":
    for i in extensions:
        bot.load_extension(i)

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('bs.도움말'))
    channel = bot.get_channel(838310425354698762)
    await channel.send('**Bread Shop**\n\n봇 상태 : <:Online:793793792406192178>')
    print(f'{bot.user} On Ready.')

@bot.command(name='리로드', aliases=['f', 'ㄹ', 'flfhem'])
async def _reload(ctx: commands.Context):
    for i in extensions:
        bot.reload_extension(i)
    await ctx.reply('리로드가 완료되었습니다.')

@bot.command(name='재시작', aliases=['리붓', '재붓', '리부팅', '재부팅'])
async def restart(ctx):
    with open('restarting.py', 'w') as f:
        f.write('import os, time\ntime.sleep(3)\nos.system("python index.py")')
    popen('python restarting.py')
    await _bot.logout()


bot.run(os.getenv("TOKEN"))