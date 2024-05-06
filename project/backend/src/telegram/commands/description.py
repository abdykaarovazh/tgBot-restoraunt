from aiogram.types import Message, FSInputFile
from project.config import config


async def send_images(message: Message, image_path, text):
    for file in image_path:
        await message.answer_photo(
            photo=FSInputFile(
                path=file
            ),
            caption=text
        )


async def description(message: Message):
    path = str(config.images.path)

    image_path = [path + 'image-1.jpg']

    text = ('"Angel Corner" - уютный ресторан с атмосферой грузинского гостеприимства.\n'
            '\n'
            'Здесь каждый гость окунется в атмосферу тепла и радушия, которая так характерна для грузинской культуры.\n'
            '\n'
            'Мы предлагаем вам насладиться изысканными блюдами грузинской кухни,'
            'приготовленными по традиционным рецептам с использованием только'
            'самых свежих и качественных ингредиентов.\n'
            '\n'
            'Наши шеф-повары умело сочетают разнообразные специи, травы и мясо,'
            'чтобы создать неповторимые вкусы, которые оставят Вас в восторге.\n'
            '\n'
            'Помимо великолепной кухни, в нашем ресторане вы найдете уютную атмосферу,'
            'дружелюбный персонал и внимательное обслуживание.\n'
            '\n'
            'Мы стремимся сделать ваше посещение незабываемым и приятным,'
            'чтобы вы хотели вернуться к нам снова и снова.\n'
            'Приходите в "Angel Corner" и погрузитесь в мир ароматов, вкусов и традиций грузинской кухни.\n'
            '\n'
            'Мы ждем Вас с распростёртыми объятиями!')

    await send_images(message, image_path, text)
