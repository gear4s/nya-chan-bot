import discord
from discord.ext import commands


class CustomContext(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)

        destination = discord.utils.get(self.guild.channels, id=self.bot.config.bot.channel.bot_commands) \
            if self.guild is not None else self.author

        if destination is None:
            destination = self.channel

        self.destination = destination

    async def reply(self, content=None, **kwargs):
        if self.guild and self.channel.id != self.bot.config.bot.channel.bot_commands:
            if content:
                content = "{1}, {0.mention}".format(self.author, content)
            else:
                content = "{0.mention}".format(self.author)

        try:
            await self.destination.send(content, **kwargs)
        except discord.Forbidden:
            await self.channel.send(content, **kwargs)
