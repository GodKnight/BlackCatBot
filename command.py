import qq
import requests
from qq.ext import commands
from config import appid, token, api_id, dbkey
import logging
import pymysql
import datetime

logging.basicConfig(level=logging.DEBUG)
client = qq.Client()
intent = qq.Intents.default()
intent.guild_messages = True
intent.at_guild_messages = False
bot = commands.Bot(command_prefix="/", intents=intent)

year=str(datetime.datetime.now().year)
month=str(datetime.datetime.now().month)
day=str(datetime.datetime.now().day)
weekday=datetime.datetime.today().weekday()
isoweekday=['一','二','三','四','五','六','天']

@bot.event
async def on_ready():
    print('服务已开启')
    startime = datetime.datetime.strptime(str(datetime.datetime.now().date() )+ '4:50', '%Y-%m-%d%H:%M')
    endtime = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '5:20', '%Y-%m-%d%H:%M')
    nowtime = datetime.datetime.now()
    if startime < nowtime < endtime:
        cywea=requests.get('https://devapi.qweather.com/v7/weather/3d?location=101120211&key='+api_id)
        lswea = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101120202&key=' + api_id)
        bcwea = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101121108&key=' + api_id)
        dgwea = requests.get('https://devapi.qweather.com/v7/weather/3d?location=101121504&key=' + api_id)
        mryj = requests.get('https://apiv3.shanbay.com/weapps/dailyquote/quote/?date='+str(datetime.datetime.today().date()))

        cytq=cywea.json()['daily'][0]['textDay']
        cymax=cywea.json()['daily'][0]['tempMax']
        cymin=cywea.json()['daily'][0]['tempMin']
        cyhum=cywea.json()['daily'][0]['humidity']

        lstq=lswea.json()['daily'][0]['textDay']
        lsmax=lswea.json()['daily'][0]['tempMax']
        lsmin=lswea.json()['daily'][0]['tempMin']
        lshum=lswea.json()['daily'][0]['humidity']

        bctq=bcwea.json()['daily'][0]['textDay']
        bcmax=bcwea.json()['daily'][0]['tempMax']
        bcmin=bcwea.json()['daily'][0]['tempMin']
        bchum=bcwea.json()['daily'][0]['humidity']

        dgtq=dgwea.json()['daily'][0]['textDay']
        dgmax=dgwea.json()['daily'][0]['tempMax']
        dgmin=dgwea.json()['daily'][0]['tempMin']
        dghum=dgwea.json()['daily'][0]['humidity']

        for channel in bot.get_all_channels():
            if channel.name == '每日播报':
                await channel.send('早上好！今天是'+year+'年'+month+'月'+day+'日，星期'+isoweekday[weekday]+'\n城阳区天气'+str(cytq)+'，温度'+str(cymin)+'°C到'+str(cymax)+'°C，湿度'+str(cyhum)+\
                                       '%\n崂山区天气'+str(lstq)+'，温度'+str(lsmin)+'°C到'+str(lsmax)+'°C，湿度'+str(lshum)+\
                                       '%\n滨城区天气'+str(bctq)+'，温度'+str(bcmin)+'°C到'+str(bcmax)+'°C，湿度'+str(bchum)+\
                                       '%\n东港区天气'+str(dgtq)+'，温度'+str(dgmin)+'°C到'+str(dgmax)+'°C，湿度'+str(dghum)+'%\n'+\
                                   str(mryj.json()['content'])+'--'+str(mryj.json()['author']))
        dbcon = pymysql.connect(host='localhost', user='root', password=dbkey, database='userdata')
        cur = dbcon.cursor()
        cur.execute('update t_user set flag=0')
        dbcon.commit()
        cur.close()
        dbcon.close()
        print('更新时间成功')


@bot.command(name="天气")
async def weather(ctx: commands.Context, city: str):
    cityreq = requests.get('https://geoapi.qweather.com/v2/city/lookup?location=' + city + '&key=' + api_id)
    cityid = cityreq.json()['location'][0]['id']
    print(cityid)

    weareq = requests.get('https://devapi.qweather.com/v7/weather/3d?location=' + str(cityid) + '&key=' + api_id)
    cityreq.encoding = 'utf-8'
    weareq.encoding = 'utf-8'
    date = weareq.json()['daily'][0]['fxDate']
    sunrise = weareq.json()['daily'][0]['sunrise']
    sunset = weareq.json()['daily'][0]['sunset']
    tempMax = weareq.json()['daily'][0]['tempMax']
    tempMin = weareq.json()['daily'][0]['tempMin']
    textDay = weareq.json()['daily'][0]['textDay']
    uvIndex = weareq.json()['daily'][0]['uvIndex']
    humidity = weareq.json()['daily'][0]['humidity']

    await ctx.reply(
        ctx.message.author.mention + city + "今日天气：" + textDay + "\n气温" + tempMin + '°C到' + tempMax + '°C\n日出时间：' \
        + sunrise + "\n日落时间：" + sunset + "\n空气湿度：" + humidity + '%\n紫外线强度：' + uvIndex)


@bot.command(name='打卡')
async def daka(ctx: commands.Context):
    dbcon = pymysql.connect(host='localhost', user='root', password=dbkey, database='userdata')
    cur = dbcon.cursor()
    cur.execute('select userpoint from t_user where userid=' + str(ctx.message.author.id))
    point = cur.fetchall()
    cur.execute('select flag from t_user where userid=' + str(ctx.message.author.id))
    flag = cur.fetchall()
    if not (flag):
        cur.execute('insert into t_user values(\'' + str(ctx.message.author.id) + '\',1,10)')
        dbcon.commit()
        await ctx.reply(ctx.message.author.mention + '打卡成功，积分+10，当前积分：10')
        cur.close()
        dbcon.close()
    else:
        if flag[0][0] == 1:
            await ctx.reply(ctx.message.author.mention + '今天已经打过卡了哦~请明天再来试试吧')
            dbcon.commit()
            cur.close()
            dbcon.close()
        else:
            ppoint = point[0][0]
            cur.execute('update t_user set userpoint=' + str(ppoint + 10) + ' where userid=\'' + str(
                ctx.message.author.id) + '\'')
            cur.execute('update t_user set flag=1 where userid=\'' + str(ctx.message.author.id) + '\'')
            dbcon.commit()
            await ctx.reply(ctx.message.author.mention + '打卡成功，积分+10，当前积分：' + str(ppoint + 10))
            cur.close()
            dbcon.close()


if __name__ == '__main__':
    bot.run(token=f"{appid}.{token}")
