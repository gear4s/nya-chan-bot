import discord
from discord.ext import commands
from types import SimpleNamespace


class CustomContextCustomItems(SimpleNamespace):
    def __getitem__(self, item_name):
        return self.__getitem__(item_name)

    # Only allow getting for attribute name, not setting
    def __getattr__(self, item_name):
        item = self.__dict__.get(item_name, None)
        if not item:
            raise AttributeError
        return item

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    __setattr__ = None


class CustomContextReply:
    # Returned by a property, this class allows replies to different destinations
    # - If command issued in DM, reply in DM
    # - If command issued in bot-command, reply in bot-command
    # - If command issued elsewhere, reply in DM, if that fails, reply in bot-command,
    #   if not found reply in same channel
    # TODO: Disable commands outside of bot-commands

    def __init__(self, context):
        self._context = context
        self._dm = False

    async def __call__(self, content=None, **kwargs):
        ctx = self._context
        if ctx.guild and ctx.channel.id != ctx.bot.config.bot.channel.bot_commands:
            if content:
                content = f"{ctx.author.mention}: {content}"
            else:
                content = f"{ctx.author.mention}"

        try:
            if self._dm is True:
                try:
                    return await ctx.author.send(content, **kwargs)
                except discord.Forbidden:
                    return await ctx.destination.send(content, **kwargs)

            return await ctx.destination.send(content, **kwargs)
        except discord.Forbidden:
            return await ctx.channel.send(content, **kwargs)

    @property
    def dm(self):
        self._dm = True
        return self


class CustomContext(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)

        destination = discord.utils.get(self.guild.channels, id=self.bot.config.bot.channel.bot_commands) \
            if self.guild is not None else self.author

        if destination is None:
            destination = self.channel

        self.destination = destination

        self._custom_items = None

    @property
    def custom(self):
        if not self._custom_items:
            self._custom_items = CustomContextCustomItems()
        return self._custom_items

    @property
    def reply(self):
        ctx = CustomContextReply(self)
        return ctx
