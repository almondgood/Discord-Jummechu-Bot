import discord
import random

CATEGORY = { "JUMMECHU" : "jumme.txt", "DOSIRAK" : "dosirak.txt"}

# 파일 r 모드로 열기
f = open('token.txt', 'r')

# readline() 함수 이용해서 한 라인씩 읽어오기
token = f.readline()
print(token)
f.close()

intents=discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():             # 봇 실행 시 실행되는 함수
    print(f'{bot.user} 에 로그인하였습니다!')

@bot.event
async def on_message(message):    # 채팅창에 메시지 입력시 실행되는 함수
    # 입력되는 메시지가 
    # !hello 이면 안녕하세요라고 반응하고 
    # !bye가 입력되는 잘가요라고 반응합니다.
    
    
    if message.content.startswith('!점메추'):  
        f = open(CATEGORY['JUMMECHU'], "r")

    elif message.content.startswith('!도시락'):
        f = open(CATEGORY['DOSIRAK'], "r")
 
    menu = []        
    while f:
        line = f.readline()
        
        if line == '':
            break
        
        menu.append(f.readline())
    print(menu)   
    await message.reply(random.choice(menu))
    f.close()

    
    
# 봇 실행
bot.run(token)