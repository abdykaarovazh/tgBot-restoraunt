from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from project.backend.src.models.tables import tables


def free_tables_list() -> ReplyKeyboardMarkup:
    kb = []

    for table_name, table_info in tables.items():
        if table_info['is_reserve'] == 'N':
            kb.append([KeyboardButton(text=f'{table_name}')])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите свободный столик'
    )

    return keyboard