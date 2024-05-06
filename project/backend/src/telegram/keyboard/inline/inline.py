from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


# Функция возвращает список Inline-кнопок с переходом на другие соц. сети
def social_links() -> InlineKeyboardMarkup:
    tg_channel_link = 'https://t.me/angel_corner_restorount/'
    instagram_link = 'https://www.instagram.com/angel_corner/'

    tg_channel = InlineKeyboardButton(text="Телеграм-канал", url=tg_channel_link)
    instagram = InlineKeyboardButton(text="Instagram", url=instagram_link)

    markup = InlineKeyboardMarkup(inline_keyboard=[[tg_channel], [instagram]])

    return markup


def menu_link() -> InlineKeyboardMarkup:
    url = 'https://restoranicafe.ru/menu'
    button = InlineKeyboardButton(text='Меню',
                                  web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

    return markup