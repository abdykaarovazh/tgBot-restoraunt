from aiogram import Bot
from aiogram.types import BotCommand

from project.backend.src.telegram.filters.lexicon.lexicon import LEXICON_MENU_COMMANDS
from project.config import config

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


# Кнопка меню, которая упаравляет основным функционалом
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description) for command, description in LEXICON_MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)