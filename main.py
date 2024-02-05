import discord
from discord.ext import commands
import logging
import random
import asyncio

jumme = []
dosirak = []
jumme_commands = ["!점메추", "!점메추가", "!도시락"]

intents=discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
discord.utils.setup_logging(level=logging.INFO, root=False)

print(discord.version_info)

with open('token.txt','r') as f:
    token=f.read() #토큰 읽어오기

with open("jumme.txt", "r", encoding="UTF-8") as f:
    while f:
        line = f.readline()
        if line == '': break
        jumme.append(line.strip())

with open("dosirak.txt", "r", encoding="UTF-8") as f:
    while f:
        line = f.readline() 
        if line == '': break         
        dosirak.append(line.strip())

@bot.event
async def on_ready():             
    print(f'{bot.user} 에 로그인하였습니다!')

@bot.command(name="점메추")
async def jummechu(ctx): 
    await ctx.send(random.choice(jumme))
    
@bot.command(name="도시락")
async def jummechu(ctx): 
    await ctx.send(random.choice(dosirak))
    
    



# TODO : 파일 입출력으로 변경
@bot.command(name="점메추가")
async def jummechuga(ctx):
    await ctx.send("추가하고 싶은 음식 이름을 입력해주세요.")
    await ctx.send("저장하시려면 `메추`, 추가하지 않으려면 `나가기`를 입력해주세요.")

    food_list = []
    while True:
        await asyncio.sleep(0.5)
        msg = (await bot.wait_for('message')).content.strip().split()
        
        if '저장' in msg:
            if len(food_list) == 0:
                await ctx.send("점심 메뉴 추가 리스트가 비어있습니다.")
                continue
            
            food_list.remove('저장')
            break
            
        if '나가기' in msg or msg in jumme_commands:
            await ctx.send("점메추가를 종료합니다.")
            return
        
        food_list += msg
        
        logging.info(food_list)
        await ctx.send(f"현재 점메 리스트 : {food_list}")
    
    jumme.append(food_list)
    logging.info(food_list)
    await ctx.send(f"저장되었습니다.")
        
    

bot.run(token) #생성한 Bot 객체에 토큰을 넣어 실행