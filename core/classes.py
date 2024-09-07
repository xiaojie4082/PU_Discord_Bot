import discord
from discord import option
from discord.ext import commands
from discord.ext import tasks

class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot