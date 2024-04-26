from aiogram.types import Message
from project.backend.src.telegram.keyboard.inline.inline import social_links


async def social(message: Message):
    try:
        markup = social_links()
        await message.answer("Тебе стало интересно узнать нашей жизни в других соц. сетях?\n"
                             "Хорошо, можешь перейти по ссылкам ниже", reply_markup=markup)
    except Exception as e:
        print("social: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")