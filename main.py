# =============== 匯入 mods ===============

from mods.weather import today_weather
from mods.punews import get_pu_news
from mods.bus import EstimateTime

# =============== 匯入必要套件 =============

# 匯入 time 套件
import time
import datetime

# 匯入讀取 .env 檔案的相關套件
import os
from dotenv import load_dotenv

# 匯入 requests 套件
import requests

# 匯入 discord 套件
import discord
from discord import option
from discord.ext import commands
from discord.ext import tasks

# 匯入 sqlite3 套件
import sqlite3

# =============== 機器人初始設定 ===============

# 創建 Discord intents 物件並啟用訊息內容 (message_content) 的接收
intents = discord.Intents.default()
intents.message_content = True

# 載入環境變數從 .env 檔案中
load_dotenv()
# 獲取 Discord 機器人令牌從環境變數
bot_token = os.getenv("DISCORD_TOKEN")
if bot_token is None:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")
# 設置命令前綴和 intents
bot = commands.Bot(command_prefix='/', intents=intents)

# =============== 機器人定時任務 ===============

# 時區設定
utc = datetime.timezone(datetime.timedelta(hours=8))

# 定時執行
times = [
    datetime.time(hour=8, minute=0, tzinfo=utc),
    datetime.time(hour=12, minute=0, tzinfo=utc),
    datetime.time(hour=20, minute=0, tzinfo=utc),
    datetime.time(hour=0, minute=0, tzinfo=utc)
]

@tasks.loop(time=times)
async def weather_background_task():
    try:
        weather_data, weather_info, icon_url = today_weather()
        current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        embed=discord.Embed(title="天氣預報", description=weather_info, color=0xffffff)
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="天氣狀況", value=weather_data[0]["Wx"]["parameterName"], inline=True)
        embed.add_field(name="最高低溫", value=weather_data[0]["MinT"]["parameterName"] + " ~ " + weather_data[0]["MaxT"]["parameterName"] + " °C", inline=True)
        embed.add_field(name="降雨機率", value=weather_data[0]["PoP"]["parameterName"] + " %", inline=True)
        # embed.add_field(name="體感狀態", value=weather[0]["CI"]["parameterName"], inline=False)
        embed.set_footer(text="更新時間：" + current_time + "\n資料來源：https://opendata.cwa.gov.tw/")

        button = discord.ui.Button(label="中央氣象署", url="https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6601300")
        view = discord.ui.View()
        view.add_item(button)

        try:
            message = await bot.get_channel(1163298141563527250).fetch_message(1168157292651360328)
            try:
                await message.edit(embed=embed, view=view)
            except discord.Forbidden:
                print("Forbidden to edit the message.")
            except discord.HTTPException as e:
                print(f"HTTP exception occurred while editing the message: {e}")
        except discord.NotFound:
            print("Message not found.")
            return
        except discord.Forbidden:
            print("Forbidden to fetch the message.")
            return
        except discord.HTTPException as e:
            print(f"HTTP exception occurred: {e}")
            return
        await message.edit(embed=embed, view=view)

        # channel = bot.get_channel(1163298141563527250)
        # await channel.send(embed=embed)
    except Exception as e:
        print(f"[weather_background_task] Error occurred: {e}")

@tasks.loop(minutes=3)
async def bus_background_task():
    try:
        Estimate = EstimateTime()

        current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        embed=discord.Embed(title="公車即時到站時間", description=
            "校門\n" + 
            ":bus: `162` `" + Estimate["162"][0] + "`\n" +
            ":bus: `301` `" + Estimate["301"][0] + "`\n" +
            ":bus: `368` `" + Estimate["368"][0] + "`\n\n" +

            "主顧樓\n" +
            ":bus: `162` `" + Estimate["162"][1] + "`\n" +
            ":bus: `301` `" + Estimate["301"][1] + "`\n" +
            ":bus: `368` `" + Estimate["368"][1] + "`\n\n" +

            "聖母堂 / 靜園餐廳\n" +
            ":bus: `162` `" + Estimate["162"][3] + "`\n" +
            ":bus: `301` `" + Estimate["301"][3] + "`\n" +
            ":bus: `368` `" + Estimate["368"][3] + "`\n"

            # "靜宜大學(專用道) - 往市區 / 往海線\n" +
            # ":bus: `300` `" + Estimate["300"][0] + " / " + Estimate["300"][1] + "`\n" +
            # ":bus: `302` `" + Estimate["302"][0] + " / " + Estimate["302"][1] + "`\n" +
            # ":bus: `303` `" + Estimate["303"][0] + " / " + Estimate["303"][1] + "`\n" +
            # ":bus: `304` `" + Estimate["304"][0] + " / " + Estimate["304"][1] + "`\n" +
            # ":bus: `305` `" + Estimate["305"][0] + " / " + Estimate["305"][1] + "`\n" +
            # ":bus: `306` `" + Estimate["306"][0] + " / " + Estimate["306"][1] + "`\n" +
            # ":bus: `307` `" + Estimate["307"][0] + " / " + Estimate["307"][1] + "`\n" +
            # ":bus: `308` `" + Estimate["308"][0] + " / " + Estimate["308"][1] + "`\n" +
            # ":bus: `309` `" + Estimate["309"][0] + " / " + Estimate["309"][1] + "`\n" +
            # ":bus: `310` `" + Estimate["310"][0] + " / " + Estimate["310"][1] + "`\n"
        , color=0xffffff)
        embed.set_footer(text="更新時間：" + current_time + "\n" + "資料來源：https://tdx.transportdata.tw")
        try:
            message = await bot.get_channel(1165339189462696118).fetch_message(1165343193324327064)
        except discord.NotFound:
            print("Message not found.")
            return
        except discord.Forbidden:
            print("Forbidden to fetch the message.")
            return
        except discord.HTTPException as e:
            print(f"HTTP exception occurred: {e}")
            return
        await message.edit(embed=embed)

        # 初始訊息
        # channel = bot.get_channel(1165339189462696118)
        # await channel.send(embed=embed)
    except Exception as e:
        print(f"[bus_background_task] Error occurred: {e}")

@tasks.loop(seconds=180)
async def news_background_task():
    try:
        title, href, summary = get_pu_news()

        conn = sqlite3.connect("data/news.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS news (title TEXT, href TEXT, summary TEXT, time TEXT)")
        cur.execute("SELECT * FROM news ORDER BY time DESC LIMIT 1")
        try:
            result = cur.fetchone()
            old_href = result[1] if result else None
        except:
            old_href = None

        if href is not None and old_href != href and title != "":
            cur.execute("INSERT INTO news (title, href, summary, time) VALUES (?, ?, ?, datetime('now', 'localtime'))", (title, href, summary))
            embed = discord.Embed(title=title, url=href, description=summary, color=0xffffff)
            embed.set_footer(text="資料來源:靜宜大學校首頁/公告總覽")
            channel = bot.get_channel(986528578197942333)
            await channel.send("<@&1148682637972602880>", embed=embed)
            try:
                await channel.send("<@&1148682637972602880>", embed=embed)
            except discord.Forbidden:
                print("Forbidden to send the message.")
            except discord.HTTPException as e:
                print(f"HTTP exception occurred while sending the message: {e}")
        conn.commit()
        conn.close()

        # 發送資料到 puhub
        # data = {'message': href, 'time': int(time.time()), 'title': title + " - 靜宜大學校首頁"}
        # response = requests.post('http://puhub.org/api/new_announcement.php', data=data)

    except Exception as e:
        print(f"[news_background_task] Error occurred: {e}")

# =============== 機器人主程式 ===============

# Bot login event handler
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    
    # 定時任務
    weather_background_task.start()
    bus_background_task.start()
    news_background_task.start()

# =============== 導入 cmds ===============

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')

for Filename in os.listdir("./cmds"):
    if Filename.endswith(".py"):
        bot.load_extension(f"cmds.{Filename[:-3]}")

# 顯示已載入的 extension
@bot.command()
async def show(ctx):

    # 顯示指令
    command_list = []
    for command in bot.commands:
        command_list.append(command.name)
    command_list_str = "\n".join(command_list)
    await ctx.send(f"\nCommands:```\n{command_list_str}```")

    # 顯示已載入的 extension
    extension_list = []
    for extension in bot.extensions:
        extension_list.append(extension)
    extension_list_str = "\n".join(extension_list)
    await ctx.send(f"\nLoaded Extensions:```\n{extension_list_str}```")

# =============== 啟動機器人 ===============

if __name__ == "__main__":
    bot.run(bot_token)