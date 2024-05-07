from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.backend.src.models.models import Tables
from project.backend.src.telegram.keyboard.reply.restoaddress import addresses


def free_tables_list(address) -> ReplyKeyboardMarkup:
    try:
        kb = []
        tables = Tables.query.filter_by(address=str(address)).all()

        for table in tables:
            if table.is_reserve == 'N':
                kb.append([KeyboardButton(text=str(f'{table.table_name}'))])

        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Выберите свободный столик',
            one_time_keyboard=True
        )
        return keyboard
    except Exception as e:
        print("free_tables_list: ", e)


# Функция, возвращающая оценки от 1 до 5
def feedback_scores() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for i in range(1, 6):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите оценку',
        one_time_keyboard=True
    )


# Функция, возвращающая клавиатуру помощи
def support_questions() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    reasons = ["Сменить время бронирования", "Вопрос по Меню", "Свой вопрос"]

    for i in reasons:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True,
                             input_field_placeholder='Выберите интересующий Вас вопрос')


# Функция, возвращающая список адресов ресторана
def resto_list() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for i in addresses:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True,
                             input_field_placeholder='Выберите адрес ресторана',
                             one_time_keyboard=True)