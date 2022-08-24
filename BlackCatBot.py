import qq
from config import appid, token
import logging

logging.basicConfig(level=logging.DEBUG)
client =qq.Client()

@client.event
async def on_message(message:qq.Message):
    print(message.content)
    if "/测试" in message.content:
        await message.reply("测试成功")

@client.event
async def on_ready():
    print("登陆成功。")

if __name__ == '__main__':
    client.run(token=f"{appid}.{token}")
