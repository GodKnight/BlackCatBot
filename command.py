import qq
import requests
from qq.ext import commands
from config import appid, token, api_id
import logging

logging.basicConfig(level=logging.DEBUG)
client = qq.Client()
intent=qq.Intents.default()
intent.guild_messages = True
intent.at_guild_messages = False
bot= commands.Bot(command_prefix="/",intents=intent)

@bot.command(name="天气")
async def weather(ctx:commands.Context,city:str):
    cityreq = requests.get('https://geoapi.qweather.com/v2/city/lookup?location='+city+'&key='+api_id)
    cityid = cityreq.json()['location'][0]['id']
    print(cityid)

    weareq = requests.get('https://devapi.qweather.com/v7/weather/3d?location='+str(cityid)+'&key='+api_id)
    cityreq.encoding='utf-8'
    weareq.encoding= 'utf-8'
    date=weareq.json()['daily'][0]['fxDate']
    sunrise=weareq.json()['daily'][0]['sunrise']
    sunset=weareq.json()['daily'][0]['sunset']
    tempMax=weareq.json()['daily'][0]['tempMax']
    tempMin=weareq.json()['daily'][0]['tempMin']
    textDay=weareq.json()['daily'][0]['textDay']
    uvIndex=weareq.json()['daily'][0]['uvIndex']
    humidity=weareq.json()['daily'][0]['humidity']

    await ctx.reply(city+"今日天气："+textDay+"\n气温"+tempMin+'°C到'+tempMax+'°C\n日出时间：'\
+sunrise+"\n日落时间："+sunset+"\n空气湿度："+humidity+'%\n紫外线强度：'+uvIndex)

if __name__ == '__main__':
    bot.run(token=f"{appid}.{token}")