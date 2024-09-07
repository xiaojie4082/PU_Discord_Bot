from mods.course import person
from mods.course import syllabus
from mods.course import search

import discord
from discord import option
from discord.ext import commands
from core.classes import Cog_Extension

import requests

class Course(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    # /尋找課程
    @commands.slash_command(name="搜尋課程", description="搜尋目前開課課程")
    @option("學期",
        description="選擇要搜尋的學期", 
        choices=["1121", "1122", "1131"], 
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
        self,
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
    @commands.slash_command(name="課程綱要", description="查詢目前課程綱要")
    @option("學期",
        description="選擇要搜尋的學期", 
        choices=["1121", "1122", "1131"], 
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
        self,
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

    # /課程餘額
    @commands.slash_command(name="課程餘額", description="查詢目前課程餘額")
    @option(
        "課程代號",
        description="請輸入課程代號",
        min_value=0,
        max_value=9999,
        required=True
    )
    async def 課程餘額(
        self,
        ctx: discord.ApplicationContext,
        課程代號: int
    ):
        course = person(課程代號)
        embed=discord.Embed(title=str(課程代號) + " - " + course["name"], color=0x00b4ff)
        embed.add_field(name="人數上限：", value=course["limit"], inline=True)
        embed.add_field(name="修課人數：", value=course["enrollment"], inline=True)
        embed.add_field(name="課程餘額：", value=course["remaining"], inline=True)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Course(bot))