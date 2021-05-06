import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

app = commands.Bot(command_prefix='/')


@app.event
# 사용자들이 함수가 끝나지않았음에도 다른 함수를 호출할 수 있기때문에 비동기
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()  # ctx는 command 객체
async def hello(ctx):
    await ctx.send('Hello, World!')

# @app.event
# async def on_message(msg):
#    await msg.add_reaction("😁")


@app.command()
async def 투표(ctx, *args):
    await ctx.send('투표 시작')
    for arg in args:
        code_block = await ctx.send(arg)
        await code_block.add_reaction("😁")


@app.command()
async def 주가(ctx, args):
    response = requests.get("http://paullab.synology.me/stock.html")

    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    메인정보 = soup.select('.main')[1]
    시가총액 = 메인정보.select('td')[0].text
    시가총액순위 = 메인정보.select('td')[1].text

    oneStep = soup.select('.main')[2]
    twoStep = oneStep.select('tbody > tr')[1:]

    날짜 = []
    종가 = []
    전일비 = []
    거래량 = []

    for i in twoStep:
        날짜.append(i.select('td')[0].text)
        종가.append(int(i.select('td')[1].text.replace(',', '')))
        전일비.append(int(i.select('td')[2].text.replace(',', '')))
        거래량.append(int(i.select('td')[6].text.replace(',', '')))

    l = []

    for i in range(len(날짜)):
        l.append({
            '날짜': 날짜[i],
            '종가': 종가[i],
            '전일비': 전일비[i],
            '거래량': 거래량[i],
        })

    if args == '시가총액':
        await ctx.send(시가총액)
    elif args == '시가총액순위':
        await ctx.send(시가총액순위)
    elif args == '전일종가':
        await ctx.send(l[0]['종가'])
    elif args == '최근한달거래':
        for i in l:
            await ctx.send(f'```날짜 : {str(i["날짜"])}\n종가 : {str(i["종가"])}\n전일비 : {str(i["전일비"])}\n거래량 : {str(i["거래량"])}```')
    else:
        await ctx.send(f'```아래와 같은 형식으로 출력이 가능합니다.\n/주가 시가총액\n/주가 시가총액순위\n/주가 전일종가\n/주가 최근한달거래```')


@app.command()
app.run('Token')
