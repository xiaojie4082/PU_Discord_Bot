import discord
from discord import option
from discord.ext import commands
from discord.ext import tasks

from core.classes import Cog_Extension

class Main(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def p(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(Main(bot))