from discord.ext import commands
import contextlib
import inspect


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        # TODO: add logger here.
        if hasattr(self, "cog_init"):
            if inspect.isawaitable(self.cog_init):
                bot.loop.run_until_complete(self.cog_init)
            else:
                self.cog_init()

    @contextlib.contextmanager
    def cursor_context(self, commit=False):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        yield cursor
        if commit:
            connection.commit()
        connection.close()

    @classmethod
    def setup(cls, bot):
        # default setup method
        bot.add_cog(cls(bot))
