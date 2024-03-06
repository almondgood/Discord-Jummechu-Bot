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

#=URL FLAG=#
NAVER = 'NAVER'
NAVER_MAP = 'NAVER_MAP'
GOOGLE = 'GOOGLE'
#=URL FLAG=#
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


#================Private Functions================#
def wrap_embed(title, description, kwargs) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    
    for name, value in kwargs.items():
        embed.add_field(name=name, value=value, inline=True)
    
    return embed

def make_url(menu, flag) -> str:
    if flag == NAVER:
        return f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={menu}"
    elif flag == NAVER_MAP:
        return f"https://map.naver.com/p/search/{menu}?searchType=place&c=13.00,0,0,0,dh"
    elif flag == GOOGLE:
        return f"https://www.google.com/search?q={menu}"
        
    return f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={menu}"
#================Private Functions================#


#================Command================#
@bot.command(name="점메추")
async def jummechu(ctx): 
    await ctx.send(random.choice(jumme))
    
@bot.command(name="도시락")
async def dosirak(ctx): 
    await ctx.send(random.choice(dosirak))
    
# 점메추 리스트
@bot.command(name="점메")
async def print_jumme(ctx):
    bot_msgs = ["", "", ""] 
    await asyncio.sleep(0.2)
    bot_msgs[0] = await ctx.send("점심메뉴 리스트를 출력합니다.")
    
    def check(message):
        return message.channel == ctx.channel
    

    while True:
        await asyncio.sleep(0.3)

        user_msg = ""
        jumme_list = {}
        
        # JUMME_PAGE 단위로 페이징
        for i, item in enumerate(random.sample(jumme, JUMME_PAGE)):
            jumme_list[i + 1] = item
        
        
        embed = wrap_embed("점메", "점심 메뉴 리스트", jumme_list)
        await bot_msgs[0].edit(embed=embed)
        logging.debug(jumme_list)
        
        if bot_msgs[1] == "":    
            bot_msgs[1] = await ctx.send('다음 리스트를 출력하려면 `다음`을 입력해 주세요.\n' + '그렇지 않다면 `나가기`를 입력해 주세요.')
            
            
        # 추가 입력 메시지 검증
        while True: 
            await asyncio.sleep(0.1)
            try:
                user_msg_object = await bot.wait_for('message', check=check, timeout=60) 
            except asyncio.TimeoutError:
                await ctx.send("시간이 초과되었습니다.\n" + "점메 출력을 종료합니다.")
                
                for bot_msg in bot_msgs:
                    await bot_msg.delete()   
                return
                
            user_msg = user_msg_object.content.strip().split()  
            
            await user_msg_object.delete()
            logging.info(user_msg)
            
            if '다음' in user_msg:
                if bot_msgs[2] != "":
                    await bot_msgs[2].delete()
                    bot_msgs[2] = ""
                break
            elif '나가기' in user_msg or user_msg[0] in jumme_commands:
                await ctx.send('점심 메뉴 출력을 종료합니다.')
                
                for bot_msg in bot_msgs:
                    await bot_msg.delete()    
                return
            else:
                if bot_msgs[2] == "":
                    bot_msgs[2] = await ctx.send("입력이 잘못되었습니다.\n" + "다시 입력해주세요.")
                
                


# TODO : 파일 입출력으로 변경
@bot.command(name="점메추가")
async def jummechuga(ctx):
    await asyncio.sleep(0.2)
    await ctx.send("추가하고 싶은 음식 이름을 입력해주세요.")
    await ctx.send("저장하시려면 `메추`, 추가하지 않으려면 `나가기`를 입력해주세요.")
    sended_list = await ctx.send(f"현재 점메 리스트 : []")


    def check(message):
        return message.channel == ctx.channel


    food_list = []
    while True:
        await asyncio.sleep(0.3)
        try:
           msg_object = await bot.wait_for('message', check=check, timeout=60) 
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과되었습니다.\n" + "점메 출력을 종료합니다.") 
            return
        
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