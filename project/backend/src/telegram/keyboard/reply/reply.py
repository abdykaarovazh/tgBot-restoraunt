from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from project.backend.src.models.tables import tables

# Функция, возвращающая клавиатуру со свободными столиками
def free_tables_list() -> ReplyKeyboardMarkup:
    kb = []

    for table_name, table_info in tables.items():
        if table_info['is_reserve'] == 'N':
            kb.append([KeyboardButton(text=f'{table_name}')])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите свободный столик',
        one_time_keyboard=True
    )
    return keyboard


# Функция, возвращающая оценки от 1 до 5
def feedback_scores() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for i in range(1, 6):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=False)