import discord
from discord.ext import commands
import os

class send_goods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_good.start()

    @tasks.loop(hours=1)
    async def send_good(self, ctx):
        channel = self.bot.get_channel(838927142561251328)

        path_dir = './Goods/'
        file_list = os.listdir(path_dir)
        

        if file_list == None:
            pass

        else:

            for i in file_list:
                with open(f'./Goods/{i}', 'r', encoding="UTF-8") as f:
                    text = f.readlines()

                lines = ''.join(text[0:])

                embed = discord.Embed(title=str('`' + await self.bot.fetch_user(int(i))) + '` 님의 요청', description=f'{lines}', color=0x00FFFF, inline=False)
                await channel.send(embed=embed)

                os.remove(f'Goods/{i}')
    
def setup(bot):
    bot.add_cog(send_goods(bot))