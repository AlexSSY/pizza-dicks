import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    SETTINGS = dict()

    @classmethod
    def fetch(cls, /, name):
        existing = cls.SETTINGS.get(name)

        if existing is None:
            env_setting = os.getenv(name)
            if env_setting is None:
                raise ValueError
            cls.SETTINGS[name] = env_setting
            return env_setting
