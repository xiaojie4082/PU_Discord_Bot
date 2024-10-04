import discord
from discord import option
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from core.classes import Cog_Extension

class React(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    # /ping
    @commands.slash_command(name="ping", description="檢查機器人的延遲")
    @commands.cooldown(1, 10, BucketType.user)
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.bot.latency * 1000)}ms")

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"此指令有冷卻時間，請在 {round(error.retry_after, 2)} 秒後再試。")

def setup(bot):
    bot.add_cog(React(bot))