import discord
from discord.ext import commands
import os
from discord.ext import tasks
import psutil

class send_goods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_good.start()

    @tasks.loop(hours=1)
    async def send_good(self):
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
                ii = i.replace(".txt", "")
                u = str(await self.bot.fetch_user(int(ii)))
                embed = discord.Embed(title=f'`{u}` 님의 요청', description=f'{lines}', color=0x00FFFF, inline=False)
                await channel.send(embed=embed)

                os.remove(f'Goods/{i}')
    
    @commands.command(name='정보')
    async def information(self, ctx):
        embed = discord.Embed(title='봇 정보', description=f'', color=0xebb145)

        user = await self.bot.fetch_user(443734180816486441)
        embed.add_field(name = '개발자', value = f'`{user}`', inline=False)
        dpyver = discord.__version__
        cpu_per = round(psutil.cpu_percent(),1) 
        mem_per = round(psutil.virtual_memory().percent,1)

        embed.add_field(name = '개발 모듈', value = f'python version 3.8.3\ndiscord.py version {dpyver}\njishaku version {jishaku.__version__}', inline=False)
        embed.add_field(name = '성능', value = f'CPU 사용량 : `{cpu_per}%`\nRAM 사용량 : `{mem_per}%`', inline=False)
        embed.add_field(name = '서버 / 유저 수', value = f'서버 수 : {len(self.bot.guilds)}\n유저 수 : {len(self.bot.users)}', inline=True)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(send_goods(bot))