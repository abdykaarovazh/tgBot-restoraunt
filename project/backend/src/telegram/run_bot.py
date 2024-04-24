from aiogram.filters import CommandStart, Command

from project.backend.src.db.db_app import app, db

from project.backend.src.telegram.commands.start import start, set_name, set_phone
from project.backend.src.telegram.commands.reserve import reserve, confirm_reserve
from project.backend.src.telegram.commands.description import description

from project.backend.src.telegram.bot import dp, bot
from project.backend.src.telegram.filters.menu import set_main_menu
from project.backend.src.telegram.states import UserStates


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Регистрация кнопки меню
    dp.startup.register(set_main_menu)

    # Регистрация команды /start
    dp.message.register(start, CommandStart())
    dp.message.register(set_name, UserStates.set_name)
    dp.message.register(set_phone, UserStates.set_phone)

    # Регистрация команды /reserve
    dp.message.register(reserve, Command('reserve'))
    dp.message.register(confirm_reserve, UserStates.reserve_table)

    # Регистрация команды /description
    dp.message.register(description, Command('description'))

    dp.run_polling(bot)