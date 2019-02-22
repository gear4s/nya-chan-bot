# import Singleton as Singleton
import pymysql
import yaml

from nyalib.bot_config import BotConfig


class Singleton(object):
    """
    This class is used to insure that you  only a single instance of the object is ever created.
    Since we're using a relative path this should be invoked from NyaChan.py first.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            cls.__contruct__(cls)
        return cls._instances[cls]

    def __contruct__(cls):
        try:
            config_stream = open('config/settings.yaml', 'r')
            cls._instances[cls].config = yaml.load(config_stream)
            config_stream.close()
        except Exception as err:
            pass

        if cls._instances[cls].config is not None:
            cls.bot = BotConfig(**cls._instances[cls].config['bot'])


class AppConfig(metaclass=Singleton):
    """
    This class will only ever create a single instance of itself, no matter how many times it's created.
    """

    def db_connection(self):
        db_config = self.config['database']
        return pymysql.connect(
            host=db_config['host'], user=db_config['user'], password=db_config['password'], db=db_config['database'],
            charset='utf8')

    @property
    def git_branch(self):
        return self.config.get('git', {}).get('branch', 'dev')
