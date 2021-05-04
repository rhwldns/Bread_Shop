from discord.ext import commands
from discord.ext import tasks
import discord
import os
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

bot.run(os.getenv("TOKEN"))