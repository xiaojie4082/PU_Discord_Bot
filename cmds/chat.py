import discord
from discord import option
from discord.ext import commands

from core.classes import Cog_Extension

import requests
import csv
import os
import sqlite3

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
        if response.status_code != 200:
            await message.edit_original_response(content="發生錯誤，請稍後再試")
        # 取得 user_id
        user_id = ctx.author.id

        # 將回應訊息寫入"sqlite"資料庫，[id, 訊息, 回應, user_id, 時間, 狀態]
        conn = sqlite3.connect("data/chat.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, 訊息 TEXT, 回應 TEXT, user_id INTEGER, 時間 TEXT, 狀態 TEXT)")
        cur.execute("INSERT INTO chat (訊息, 回應, user_id, 時間, 狀態) VALUES (?, ?, ?, datetime('now', 'localtime'), 'no_reply_yet')", (訊息, response.text, user_id))
        conn.commit()
        # 紀錄此次對話的id
        chat_id = cur.lastrowid
        conn.close()

        view = discord.ui.View()
        # 建立三個狀態按鈕(resolved, unresolved, report)
        button_reprot = discord.ui.Button(label="回報錯誤", style=discord.ButtonStyle.danger)
        async def button_reprot_callback(interaction, chat_id=chat_id):
            conn = sqlite3.connect("data/chat.db")
            cur = conn.cursor()
            cur.execute("UPDATE chat SET 狀態 = 'reported' WHERE id = ?", (chat_id,))
            conn.commit()
            conn.close()
            message_text = "```我們已收到您的錯誤已回報，回報編號為 " + str(chat_id) + "。如有任何疑問，請提供此編號與管理員聯繫，謝謝您！```"
            await interaction.response.send_message(message_text, ephemeral=True)
        button_reprot.callback = button_reprot_callback
        view.add_item(button_reprot)
        button_resolved = discord.ui.Button(label="已解決", style=discord.ButtonStyle.success)
        async def button_resolved_callback(interaction, chat_id=chat_id):
            conn = sqlite3.connect("data/chat.db")
            cur = conn.cursor()
            cur.execute("UPDATE chat SET 狀態 = 'resolved' WHERE id = ?", (chat_id,))
            conn.commit()
            conn.close()
            message_text = "```很開心能解決你的問題，感謝您的使用！```"
            await interaction.response.send_message(message_text, ephemeral=True)
        button_resolved.callback = button_resolved_callback
        view.add_item(button_resolved)
        button_unresolved = discord.ui.Button(label="未解決", style=discord.ButtonStyle.secondary)
        async def button_unresolved_callback(interaction, chat_id=chat_id):
            conn = sqlite3.connect("data/chat.db")
            cur = conn.cursor()
            cur.execute("UPDATE chat SET 狀態 = 'unresolved' WHERE id = ?", (chat_id,))
            conn.commit()
            conn.close()
            message_text = "```很抱歉未能解決您的問題，我會繼續努力改進！```"
            await interaction.response.send_message(message_text, ephemeral=True)
        button_unresolved.callback = button_unresolved_callback
        await message.edit_original_response(content=response.text, view=view)

def setup(bot):
    bot.add_cog(Chat(bot))