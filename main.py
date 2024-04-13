# =============== 匯入相關套件 ===============

# 匯入 course 模組
from course import person
from course import syllabus
from course import search

# 匯入 weather 模組
from weather import today_weather

# 匯入 punew 模組
from punews import get_pu_news

# 匯入 time 模組
import time
import datetime

# 匯入讀取 .env 檔案的相關套件
import os
from dotenv import load_dotenv

# 匯入 requests 套件
import requests
import json

# 匯入 threading 套件
import threading

# 匯入 discord 套件
import discord
from discord import option
from discord.ext import commands
from discord.ext import tasks
import threading

# =============== 機器人初始設定 ===============

# 創建 Discord intents 物件並啟用訊息內容 (message_content) 的接收
intents = discord.Intents.default()
intents.message_content = True

# 載入環境變數從 .env 檔案中
load_dotenv()
# 獲取 Discord 機器人令牌從環境變數
bot_token = os.getenv("DISCORD_TOKEN")
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

        message = await bot.get_channel(1163298141563527250).fetch_message(1168157292651360328)
        await message.edit(embed=embed, view=view)

        # 初始訊息
        # channel = bot.get_channel(1163298141563527250)
        # await channel.send(embed=embed)
    except Exception as e:
        print(f"[weather_background_task] Error occurred: {e}")

@tasks.loop(minutes=1)
async def bus_background_task():
    try:
        with open(os.getenv("BUS_PATH"), 'r') as f:
            Estimate = json.load(f)

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
        message = await bot.get_channel(1165339189462696118).fetch_message(1165343193324327064)
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

        with open(os.getenv("NEWS_PATH"), "r") as file:
            file_content = file.read()
            
        if file_content != href:
            with open(os.getenv("NEWS_PATH"), "w") as file:
                file.write(href)
            
            data = {'message': href, 'time': int(time.time()), 'title': title + " - 靜宜大學校首頁"}
            response = requests.post('http://puhub.org/api/new_announcement.php', data=data)

            embed = discord.Embed(title=title, url=href, description=summary+" <@&1148682637972602880>", color=0xffffff)
            embed.set_footer(text="資料來源:靜宜大學校首頁/公告總覽")
            channel = bot.get_channel(986528578197942333)
            await channel.send(embed=embed)

    except Exception as e:
        print(f"[news_background_task] Error occurred: {e}")

# =============== 機器人主程式 ===============

# Logged in
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # 定時任務
    weather_background_task.start()
    bus_background_task.start()
    news_background_task.start()

    # 初始訊息 - 社群網站
    # embed=discord.Embed(title="PUHub - 你在校園生活中不可或缺的夥伴", color=0xffffff)
    # embed.set_image(url="https://cdn.discordapp.com/attachments/1152904955099893820/1176784764464799764/image.png?ex=65702137&is=655dac37&hm=e979775bcd00996ef7ebb608fda371a79e887105949f054046cbb2973cbded26&")
    # view = discord.ui.View()
    # button = discord.ui.Button(label="社群網站", url="https://puhub.org/")
    # view.add_item(button)
    # button = discord.ui.Button(label="匿名留言", url="https://puhub.org/services_send.php")
    # view.add_item(button)
    # button = discord.ui.Button(label="選課評價", url="https://puhub.org/services_courses.php")
    # view.add_item(button)
    # button = discord.ui.Button(label="實用連結", url="https://puhub.org/services_resource.php")
    # view.add_item(button)
    # channel = bot.get_channel(1141266582601998416)
    # await channel.send(embed=embed, view=view)

# /ping
@bot.slash_command(name="ping", description="檢查機器人的延遲") 
async def ping(ctx): 
    start = time.time()
    message = await ctx.respond('等待中...')
    end = time.time()
    latency = (end - start) * 1000
    await message.edit_original_response(content=f'{latency:.1f} ms')

# /gs_chat
@bot.slash_command(name='chat', description='gemini-pro')
@option(
    "訊息",
    description="請輸入訊息或問題",
    required=True
)
async def chat(
    ctx: discord.ApplicationContext,
    訊息: str
):
    message = await ctx.respond('正在處理中...')
    response = requests.post('http://localhost:5000/gschat', json={'message':訊息})
    await message.edit_original_response(content=response.text)

# /freshman_chat
@bot.slash_command(name='freshman', description='freshman gemini-pro')
@option(
    "訊息",
    description="請輸入訊息或問題",
    required=True
)
async def freshman(
    ctx: discord.ApplicationContext,
    訊息: str
):
    message = await ctx.respond('正在處理中...')
    response = requests.post('http://localhost:5000/freshmanchat', json={'message':訊息})
    await message.edit_original_response(content=response.text)

# /尋找課程
@bot.slash_command(name="搜尋課程", description="搜尋目前開課課程")
@option("學期",
    description="選擇要搜尋的學期", 
    choices=["1111", "1112", "1121", "1122"], 
    required=True   
)
@option("類別",
    description="選擇要搜尋的類別", 
    choices=["老師", "課程"], 
    required=True
)
@option(
    "關鍵字",
    description="請輸入搜尋關鍵字",
    required=True
)
async def 尋找課程(
    ctx: discord.ApplicationContext,
    學期: str,
    類別: str,
    關鍵字: str
):
    message = await ctx.respond('正在處理中...')
    course_data, url = search(學期,類別,關鍵字)
    
    embed=discord.Embed(title="搜尋到 " + str(len(course_data)) + " 筆資料，以下是搜尋結果。", color=0x00b4ff)
    index = 0
    for course in course_data:
        index = index + 1
        if index > 10:
            embed.set_footer(text="搜尋結果上限為十筆，請使用更詳細的關鍵字進行搜尋。")
            break
        embed.add_field(name="[" + course['選課代號'] + "] [" + course['修別'] + "] [" + course['上課班級'] + "]  [" + course['上課時間地點'] + "]", value=course['授課老師'] + " - " + course['科目名稱'], inline=False)
    view = discord.ui.View()
    button = discord.ui.Button(label="選課查詢", url=url)
    view.add_item(button)
    await message.edit_original_response(embed=embed, view=view)

# /課程綱要
@bot.slash_command(name="課程綱要", description="查詢目前課程綱要")
@option("學期",
    description="選擇要搜尋的學期", 
    choices=["1111", "1112", "1121", "1122"], 
    required=True   
)
@option(
    "課程代號",
    description="請輸入課程代號",
    min_value=0,
    max_value=9999,
    required=True
)
async def 課程綱要(
    ctx: discord.ApplicationContext,
    學期: str,
    課程代號: int
):
    course = syllabus(學期, str(課程代號))
    embed=discord.Embed(title="[" + course["name"] + "] [" + course["instructor"] + "] [" + course["time"] + "]", color=0x00b4ff)
    embed.add_field(name="課程簡介：", value="```" + course["description"] + "```", inline=False)
    embed.add_field(name="評分方式：", value="```" + course["grading"] + "```", inline=False)
    embed.add_field(name="課程評論：", value=course["evaluation"], inline=False)
    embed.add_field(name="AI 分析：", value="```正在生成中...```", inline=False)
    
    view = discord.ui.View()
    button = discord.ui.Button(label="課程綱要", url=course["url"])
    view.add_item(button)
    button = discord.ui.Button(label="課程評價", url="https://puhub.org/services_courses.php?course=" + course["name"] + "&teacher=" + course["instructor"])
    view.add_item(button)

    message = await ctx.respond(embed=embed, view=view)

    gs = requests.post('http://localhost:5000/gschat', json={'message':course["ai_mes"]})
    embed.remove_field(3)
    embed.add_field(name="AI 分析：", value="```"+gs.text+"```", inline=False)
    await message.edit_original_response(embed=embed, view=view)

    # 多線程
    # def gs_thread():
    #     gs = "```" + gs_chat(course["ai_mes"]) + "```"
    #     embed.remove_field(3)
    #     embed.add_field(name="AI 分析：", value=gs, inline=False)
    #     message.edit_original_response(embed=embed, view=view)
    
    # thread = threading.Thread(target=gs_thread)
    # thread.start()

# /課程餘額
@bot.slash_command(name="課程餘額", description="查詢目前課程餘額")
@option(
    "課程代號",
    description="請輸入課程代號",
    min_value=0,
    max_value=9999,
    required=True
)
async def 課程餘額(
    ctx: discord.ApplicationContext,
    課程代號: int
):
    course = person(課程代號)
    embed=discord.Embed(title=str(課程代號) + " - " + course["name"], color=0x00b4ff)
    embed.add_field(name="人數上限：", value=course["limit"], inline=True)
    embed.add_field(name="修課人數：", value=course["enrollment"], inline=True)
    embed.add_field(name="課程餘額：", value=course["remaining"], inline=True)
    await ctx.respond(embed=embed)

# =============== 啟動機器人 ===============

bot.run(bot_token)