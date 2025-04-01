from pydantic import BaseSettings


class Setting(BaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


setting = Setting()