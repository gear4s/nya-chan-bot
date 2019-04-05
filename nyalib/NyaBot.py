import discord
from discord.ext import commands
from nyalib.config import AppConfig
from nyalib.CustomContext import CustomContext
from nyalib.HelpCommand import Command


class ThrowawayException(Exception):
    pass


class NyaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # TODO: Change self.config to use a cog
        self.config = AppConfig()
        kwargs.update(command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                      help_command=Command(dm_help=True))
        super().__init__(*args, **kwargs)

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=CustomContext)
        await self.invoke(ctx)

    async def on_ready(self):
        print('######################################################')
        print('#                      Nya Chan                      #')
        print('######################################################')
        print('Discord.py version : ' + discord.__version__)
        print('Bot User : ' + str(self.user))
        app_infos = await self.application_info()
        self.owner_id = app_infos.owner.id
        print('Bot Owner : ' + str(self.owner_id))
        url = discord.utils.oauth_url(app_infos.id)
        print('Oauth URL : ' + url)
