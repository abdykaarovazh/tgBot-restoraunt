from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app

from project.backend.src.telegram.states import UserStates
from project.backend.src.telegram.keyboard.reply.reply import free_tables_list, resto_list

from project.backend.src.models.models import Users, Tables
from project.backend.src.telegram.bot import logger


async def reserve(message: Message, state: FSMContext):
    try:
        with app.app_context():
            tg_username = message.from_user.username
            is_user = Users.get_current(tg_username)
            if is_user:
                await message.answer("Рады, что Вы решили забронировать столик!\n"
                                     "Выберите адрес ресторана, который планируете посетить!",
                                     reply_markup=resto_list())
                await state.set_state(UserStates.reserve_table)
            else:
                await message.answer("Для того, чтобы зарезервировать столик, "
                                     "Вам потребуется сначала пройти небольшую регистрацию по команде /start")
    except Exception as e:
        logger.exception("reserve", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def reserve_address(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(address=message.text)
            await message.answer(f"Отлично, напишите, пожалуйста, дату, в которую Вы планируете "
                                 f"посетить наш ресторан!\n"
                                 f"\n"
                                 f"Формат даты должен выглядеть вот так: <b>24.05.2024</b>")
            await message.answer("Также настоятельно прошу Вас написать <b>актуальную дату</b>. "
                                 "Если Вы напишете дату <b>ранее, чем сегодняшний день</b>, "
                                 "то столик забронировать <b>не получится</b>")

            await state.set_state(UserStates.set_time)
    except Exception as e:
        logger.exception("reserve_address: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def set_time_reserve(message: Message, state: FSMContext):
    try:
        await state.update_data(date_reserve=message.text)
        await message.answer("Так, хорошо, а теперь напишите, пожалуйста, время, "
                             "в которое планируете посетить ресторан в формате: <b>18:00</b>")
        await state.set_state(UserStates.set_table)
    except Exception as e:
        print("set_time_reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def set_table(message: Message, state: FSMContext):
    try:
        await state.update_data(time_reserve=message.text)
        get_data = await state.get_data()
        address = str(get_data.get('address'))
        print(address)

        await message.answer("Отлично, а теперь выберите, пожалуйста, <b>свободный столик</b> в списке ниже",
                             reply_markup = await free_tables_list(address, message.from_user.id))
        await state.set_state(UserStates.confirm_reserve_table)
    except Exception as e:
        logger.exception("set_time_reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def confirm_reserve(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(table_name=message.text)

            get_data = await state.get_data()

            address = get_data.get('address')
            table = get_data.get('table_name')
            time = get_data.get('time_reserve')
            date = get_data.get('date_reserve')

            table_name = table[:9]  # Берем только необходимое название стола без количества мест

            reserve_table = Tables.reserve(address, table_name, message.from_user.username, time, date)

            await message.answer(f"Отлично! {reserve_table.table_name} забронирован!\n"
                                 f"Через несколько минут с тобой свяжется Администратор ресторана,"
                                 f"чтобы подтвердить бронь!\n"
                                 f"\n"
                                 f"Увидимся :)"
                                 f"\n"
                                 f"Обязательно оставь отзыв после того, как "
                                 f"посетишь наш ресторан по команде /feedback")
    except Exception as e:
        logger.exception("confirm_reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()
