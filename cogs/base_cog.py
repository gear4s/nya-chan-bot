from discord.ext import commands
import contextlib


class BaseCogMeta(commands.CogMeta):
    def __new__(mcs, *args, **kwargs):
        name, bases, attrs = args
        new_cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        new_cls.bot = None
        new_cls.config = None
        return new_cls

    def __init__(cls, *args, **kwargs):
        def custom_init(self, *init_args, **init_kwargs):
            if len(init_args) != 0:
                bot = init_args[0]
                cls.bot = bot
                cls.config = bot.config
                cls.__cog__init__(self)
                bot.add_cog(self)

        cls.__cog__init__ = cls.__init__
        cls.__init__ = custom_init
        super().__init__(*args)


class BaseCog(commands.Cog, metaclass=BaseCogMeta):
    @contextlib.contextmanager
    def cursor_context(self, commit=False):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        yield cursor
        if commit:
            connection.commit()
        connection.close()
