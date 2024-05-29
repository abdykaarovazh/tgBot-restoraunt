from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.backend.src.models.models import Tables
from project.backend.src.telegram.keyboard.reply.restoaddress import addresses
from project.backend.src.db.db_app import app
from project.backend.src.telegram.bot import bot


async def free_tables_list(address: str, user_id) -> ReplyKeyboardMarkup:
    try:
        with app.app_context():
            kb = []
            tables = Tables.query.filter_by(address=address).all()

            for table in tables:
                if table.is_reserve == 'N':
                    kb.append([KeyboardButton(text=f'{table.table_name} на {table.place_count} мест(а)')])
            if tables is None:
                await bot.send_message(user_id,
                                       "К сожалению, свободных столиков на данный момент нет, попробуйте позднее или "
                                       "свяжитесь с Администратором ресторана для уточнения информации")

            keyboard = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            return keyboard
    except Exception as e:
        print("free_tables_list: ", e)


# Выводит клавиатуру со списком забронированных столиков пользователем
def reserved_tables_by_user(user) -> ReplyKeyboardMarkup:
    with app.app_context():
        kb = []
        tables = Tables.get_all(user, 'Y')
        for table in tables:
            kb.append([KeyboardButton(text=f"{table.table_name} по адресу {table.address}")])

        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        return keyboard


# Функция, возвращающая оценки от 1 до 5
def feedback_scores() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for i in range(1, 6):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


# Функция, возвращающая клавиатуру помощи
def support_questions() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    reasons = ["Сменить время бронирования", "Вопрос по Меню", "Свой вопрос", "Отменить бронь"]

    for i in reasons:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


# Функция, возвращающая список адресов ресторана
def resto_list() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for i in addresses:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)
