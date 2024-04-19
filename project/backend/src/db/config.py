from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str


@dataclass
class TgBot:
    token: str

@dataclass
class FlaskConfig:
    flask_host: str
    flask_port: int

@dataclass
class Config:
    tg_bot: TgBot
    db:     DatabaseConfig
    flask:  FlaskConfig


env: Env = Env()
env.read_env()

config = Config(
    tg_bot = TgBot(
        token = env('BOT_TOKEN')
    ),
    db = DatabaseConfig(
        db_name = env('DB_NAME'),
        db_host = env('DB_HOST'),
        db_port = env('DB_PORT'),
        db_user = env('DB_USER'),
        db_pass = env('DB_PASSWORD')
    ),
    flask = FlaskConfig(
        flask_host = env('FLASK_HOST'),
        flask_port = env('FLASK_PORT')
    )
)
