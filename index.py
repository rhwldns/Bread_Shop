from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['bs.', 'bs. '], help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} On Ready.')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('bs.도움말'))
    print(bot.ws)


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))