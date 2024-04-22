from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app
from project.backend.src.models.models import Users
from project.backend.src.telegram.states import UserStates


async def start(message: Message, state: FSMContext):
    try:
        with app.app_context():
            tg_username = message.from_user.username
            is_user = Users.get_current(tg_username=tg_username)
            markup = None
            if is_user:
                await message.answer("Salami! Рады, что ты снова решил обратиться к нам!\n"
                                     "Хочешь забронировать столик? Давай посмотрим свободные столики.\n",
                                     reply_markup=markup)
            else:
                await message.answer("Salami! Рады, что ты решил(а) мной воспользоваться!\n"
                                     "Давай зарегистрируем тебя у нас, чтобы ты мог без "
                                     "повторной регистрации пользоваться"
                                     "моими возможностями!")
                await message.answer("Напиши, пожалуйста, своё имя?")
                await state.set_state(UserStates.set_name)
    except Exception as e:
        print("START: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def set_name(message: Message, state: FSMContext):
    try:
        await state.update_data(username=message.text)
        await state.set_state(UserStates.set_phone)
        await message.answer("Отлично! Теперь напиши свой номер телефона для связи Администрации ресторана с тобой")
    except Exception as e:
        print("set name: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def set_phone(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(userphone=message.text)
            get_data = await state.get_data()

            username = get_data.get('username')
            userphone = get_data.get('userphone')

            new_user = Users.create(
                user_name=username,
                tg_user_id=message.from_user.id,
                tg_username=message.from_user.username,
                user_phone=userphone
            )
            print(new_user)

            await message.answer(f"Ты молодец, {username}! А теперь давай я тебе покажу что я имею.\n"
                                 "Обрати внимание на кнопку Меню слева, рядом с полем ввода!"
                                 "\n"
                                 "Mogesalmebit, chemo megobaro!")
    except Exception as e:
        print("set phone: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
