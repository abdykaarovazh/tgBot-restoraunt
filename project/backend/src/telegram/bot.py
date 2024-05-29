from aiogram import Bot, Dispatcher
from project.config import config
import logging

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)