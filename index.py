from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['bs.', 'bs. '], help_command=None, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('bs.도움말'))
    channel = bot.get_channel(838310425354698762)
    await channel.send('**Bread Shop**\n\n봇 상태 : <:Online:793793792406192178>')
    print(f'{bot.user} On Ready.')


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))