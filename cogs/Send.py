import discord
from discord.ext import commands
import os
from discord.ext import tasks
import psutil
import string
from pymongo import MongoClient

coll = MongoClient('mongodb://localhost:27017/').Bread_Shop.user

class send_goods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_good.start()

    @tasks.loop(hours=1)
    async def send_good(self):
        await self.bot.wait_until_ready()
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
                uu = await self.bot.get_user(int(ii))

                embed = discord.Embed(title=f'`{u}` 님의 요청', description=f'{lines}', color=0xebb145, inline=False)
                embed.set_footer(text=f'ㅣ{str(ii)}', icon_url=uu.avatar_url)
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
    
    @commands.command(name='주문')
    async def order(self, ctx, *, content=None):
        if content == None:
            embed = discord.Embed(title=':warning: 주의', description='`bs.주문` 명령어의 올바른 사용 방법 :\n`bs.주문 <내용 + 빵의 종류>` 입니다.', color=0xE1AA00)
            embed.add_field(name='추가 기입 항목', value='쿠키 : 일정의 코드\n빵 : 한 코드 파일\n케이크 : 봇 주문제작 등', inline=False)
            return await ctx.send(embed=embed)
        
        else:
            with open(f'Goods/{str(ctx.author.id)}.txt', 'w', encoding="UTF-8") as f:
                f.write(content)

            embed = discord.Embed(title='완료', description='주문이 완료되었습니다.', color=0x00FFFF)
            return await ctx.send(embed=embed)
    
    @commands.is_owner()
    @commands.command(name='목록')
    async def order_list(self, ctx):
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
                uu = await self.bot.get_user(int(ii))

                d = coll.find_one({"_id": str(ii)})

                embed = discord.Embed(title=f'`{u}` 님의 요청', description=f'{lines}', color=0xebb145, inline=False)
                embed.set_footer(text=f'ㅣ{str(ii)}\nUUID : {d['uuid']}', icon_url=uu.avatar_url)
                await channel.send(embed=embed)

                os.remove(f'Goods/{i}')
    
    @commands.command(name='완료')
    async def order_done(self, ctx, id_uuid=None, *, content=None):
        if id_uuid == None or content == None or id_uuid and content == None::
            embed = discord.Embed(title=':warning: 주의', description='`bs.완료` 명령어의 올바른 사용 방법 :\n`bs.완료 <유저의 ID or UUID> <전달할 내용>` 입니다.', color=0xE1AA00)
            return await ctx.send(embed=embed)
        


    
def setup(bot):
    bot.add_cog(send_goods(bot))