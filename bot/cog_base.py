from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
