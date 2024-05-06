from aiogram.types.message import Message
from project.backend.src.telegram.keyboard.inline.inline import menu_link


async def menu_restorer(message: Message):
    markup = menu_link()
    await message.answer('Если тебе интересно, что в нашем Меню ресторана,'
                         'то ты сможешь взяглянуть по ссылке ниже.\n'
                         '\n'
                         'По любым другим вопросам ты сможешь обратиться по команде /support', reply_markup=markup)