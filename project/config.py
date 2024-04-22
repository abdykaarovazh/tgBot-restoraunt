from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_name: str

@dataclass
class TgBot:
    token: str

@dataclass
class FlaskConfig:
    flask_host: str
    flask_port: int

@dataclass
class SSLCert:
    ssl_path: str
    ssl_cert: str
    ssl_key:  str

@dataclass
class Config:
    tg_bot: TgBot
    db:     DatabaseConfig
    flask:  FlaskConfig
    ssl:    SSLCert


env: Env = Env()
env.read_env()

config = Config(
    tg_bot = TgBot(
        token = env('BOT_TOKEN')
    ),
    db = DatabaseConfig(
        db_name = env('DB_NAME'),
    ),
    flask = FlaskConfig(
        flask_host = env('FLASK_HOST'),
        flask_port = env('FLASK_PORT')
    ),
    ssl = SSLCert(
        ssl_path = env('SSL_PATH'),
        ssl_cert = env('SSL_CERT_FILE'),
        ssl_key  = env('SSL_KEY_FILE')
    )
)
