import discord
from discord.ext import commands
import logging
import random
import asyncio


#================Initialization================#
logging.basicConfig(
    filename = 'app.log',
    filemode='w',
    level=logging.DEBUG,
    encoding='UTF-8'
)

#====Variables====#
jumme = []
dosirak = []
jumme_commands = ["!점메", "!점메추", "!점메추가", "!도시락"]
JUMME_PAGE = 10
#====Variables====#

#====Bot settings====#
intents=discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
discord.utils.setup_logging(level=logging.DEBUG, root=False)

print(discord.version_info)
#====Bot settings====#

@bot.event
async def on_ready():             
    print(f'{bot.user} 에 로그인하였습니다!')
#================Initialization================#




#================File Open================#
with open('token.txt','r') as f:
    token=f.read() #토큰 읽어오기

with open("jumme_default.txt", "r", encoding="UTF-8") as f:
    while f:
        line = f.readline()
        if line == '': break
        jumme.append(line.strip())

with open("dosirak_default.txt", "r", encoding="UTF-8") as f:
    while f:
        line = f.readline() 
        if line == '': break         
        dosirak.append(line.strip())
#================File Open================#




#================Command================#
@bot.command(name="점메추")
async def jummechu(ctx): 
    await ctx.send(random.choice(jumme))
    
@bot.command(name="도시락")
async def dosirak(ctx): 
    await ctx.send(random.choice(dosirak))
    

                
                


# TODO : 파일 입출력으로 변경
@bot.command(name="점메추가")
async def jummechuga(ctx):
    await asyncio.sleep(0.2)
    await ctx.send("추가하고 싶은 음식 이름을 입력해주세요.")
    await ctx.send("저장하시려면 `메추`, 추가하지 않으려면 `나가기`를 입력해주세요.")
    sended_list = await ctx.send(f"현재 점메 리스트 : []")


    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel


    food_list = []
    while True:
        await asyncio.sleep(0.3)
        msg_object = await bot.wait_for('message', check=check) 
        user_msg = msg_object.content.strip().split()  
        await msg_object.delete()
        
        
        # 메뉴 리스트 저장
        if '메추' in user_msg:
            if len(food_list) == 0:
                await ctx.send("점심 메뉴 추가 리스트가 비어있습니다.")
                continue
            else: break
            
        if '나가기' in user_msg or user_msg[0] in jumme_commands:
            await ctx.send("점메추가를 종료합니다.")
            return
        
        
        food_list += user_msg
        logging.debug(food_list)
        await sended_list.edit(content=f"현재 점메 리스트 : {food_list}")
    

    jumme.append(food_list)
    logging.debug(food_list)
    await ctx.send(f"저장되었습니다.")
#================Command================#        


bot.run(token) #생성한 Bot 객체에 토큰을 넣어 실행