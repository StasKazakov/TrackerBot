from dataclasses import dataclass
from typing import Optional

from environs import Env


    # For SQLAlchemy
    # def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> URL:
    #     if not host:
    #         host = self.host
    #     if not port:
    #         port = self.port
    #     uri = URL.create(
    #         drivername=f"postgresql+{driver}",
    #         username=self.user,
    #         password=self.password,
    #         host=host,
    #         port=port,
    #         database=self.database,
    #     )
    #     return uri.render_as_string(hide_password=False)


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous
    db: DbConfig 


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=env.list("ADMINS"),
        ),

        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('MYSQL_PASSWORD'),
            user=env.str('MYSQL_USER'),
            database=env.str('MYSQL_DB')
        ),
        

        # redis=RedisConfig(
        #     redis_pass=env.str("REDIS_PASSWORD"),
        #     redis_port=env.int("REDIS_PORT"),
        #     redis_host=env.str("REDIS_HOST"),
        # ),

        misc=Miscellaneous()
    )
