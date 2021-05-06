import discord
from discord.ext import commands

app = commands.Bot(command_prefix='/')


@app.event
# 사용자들이 함수가 끝나지않았음에도 다른 함수를 호출할 수 있기때문에 비동기
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()  # ctx는 command 객체
async def hello(ctx):
    await ctx.send('Hello, World!')


@app.command()
app.run('ODM5NzgxMTM1MjMwODI4NTg1.YJOpIQ.PBpnIbvFRviX3GEI0gOxujyQYrA')
