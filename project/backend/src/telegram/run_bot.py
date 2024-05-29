from aiogram.filters import CommandStart, Command
from aiogram import F
import asyncio

from project.backend.src.db.db_app import app, db
from project.backend.src.models.models import Users
from project.backend.src.telegram.commands.start import start, set_name, set_phone
from project.backend.src.telegram.commands.menu_rest import menu_restorer
from project.backend.src.telegram.commands.reserve import (reserve, reserve_address, confirm_reserve,
                                                           set_time_reserve, set_table)
from project.backend.src.telegram.commands.description import description
from project.backend.src.telegram.commands.feedback import feedback, write_feedback, write_score
from project.backend.src.telegram.commands.social import social
from project.backend.src.telegram.commands.support import (support, change_time, menu_questions,
                                                           resto_addresses, self_questions,
                                                           quit_reserve, confirm_quit, change_date_time,
                                                           vote_table_before_change_time)

from project.backend.src.telegram.bot import dp, bot
from project.backend.src.telegram.filters.menu import set_main_menu
from project.backend.src.telegram.utils.alert import check_reservations_alert
from project.backend.src.telegram.states import UserStates


async def on_startup():
    with app.app_context():
        tasks = [check_reservations_alert(user.tg_user_id) for user in Users.query.all()]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Инициализируем таблицы в базе данных
    with app.app_context():
        db.create_all()

    # Регистрация списка кнопок меню
    dp.startup.register(set_main_menu)
    # Это регистрирует уведомление о брони.
    # ЕСЛИ НУЖНО ЗАСКРИНИТЬ УВЕДОМЛЕНИЕ, ТО РАСКОММЕНТИРОВАТЬ СТРОЧКУ НИЖЕ, УДАЛИВ РЕШЕТКУ
    #dp.startup.register(on_startup)

    # Регистрация команды /start
    dp.message.register(start, CommandStart())
    dp.message.register(set_name, UserStates.set_name)
    dp.message.register(set_phone, UserStates.set_phone)

    # Регистрация команды /menu
    dp.message.register(menu_restorer, Command('menu'))

    # Регистрация команды /reserve
    dp.message.register(reserve, Command('reserve'))
    dp.message.register(reserve_address, UserStates.reserve_table)
    dp.message.register(set_time_reserve, UserStates.set_time)
    dp.message.register(set_table, UserStates.set_table)
    dp.message.register(confirm_reserve, UserStates.confirm_reserve_table)

    # Регистрация команды /description
    dp.message.register(description, Command('description'))

    # Регистрация команды /feedback
    dp.message.register(feedback, Command('feedback'))
    dp.message.register(write_feedback, UserStates.feedback_text)
    dp.message.register(write_score, UserStates.feedback_score)

    # Регистрация команды /social
    dp.message.register(social, Command('social'))

    # Регистрация команды /support
    dp.message.register(support, Command('support'))
    dp.message.register(change_time, F.text.lower() == "сменить время бронирования")
    dp.message.register(vote_table_before_change_time, UserStates.vote_table_before_change_time)
    dp.message.register(change_date_time, UserStates.change_date_time)
    dp.message.register(menu_questions, F.text.lower() == "вопрос по меню")
    dp.message.register(resto_addresses, UserStates.resto_address)
    dp.message.register(self_questions, F.text.lower() == "свой вопрос")
    dp.message.register(quit_reserve, F.text.lower() == "отменить бронь")
    dp.message.register(confirm_quit, UserStates.confirm_quit)

    # Запускаем бота на локальном сервере
    dp.run_polling(bot)