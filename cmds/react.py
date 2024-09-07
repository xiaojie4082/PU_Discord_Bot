import discord
from discord import option
from discord.ext import commands
from discord.ext import tasks

from core.classes import Cog_Extension

class React(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    # /ping
    @commands.slash_command(name="ping", description="檢查機器人的延遲") 
    async def ping(self, ctx): 
        await ctx.respond(f"{round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(React(bot))