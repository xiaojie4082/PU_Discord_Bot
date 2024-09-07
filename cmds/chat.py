import discord
from discord import option
from discord.ext import commands

from core.classes import Cog_Extension

import requests

class Chat(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    # /chat
    @commands.slash_command(name='chat', description='問問小幫手')
    @option(
        "訊息",
        description="請輸入訊息或問題",
        required=True
    )
    async def chat(
        self,
        ctx: discord.ApplicationContext,
        訊息: str
    ):
        message = await ctx.respond('正在處理中...')
        response = requests.post('http://localhost:5000/puchat', json={'message':訊息})
        view = discord.ui.View()
        button = discord.ui.Button(label="⭕ 已解決", style=discord.ButtonStyle.green)
        view.add_item(button)
        button = discord.ui.Button(label="❌ 未解決", style=discord.ButtonStyle.green)
        view.add_item(button)
        button = discord.ui.Button(label="回報錯誤", style=discord.ButtonStyle.danger)
        view.add_item(button)
        await message.edit_original_response(content=response.text, view=view)

def setup(bot):
    bot.add_cog(Chat(bot))