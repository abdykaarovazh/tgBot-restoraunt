from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app

from project.backend.src.telegram.states import UserStates
from project.backend.src.telegram.keyboard.reply.reply import free_tables_list, resto_list

from project.backend.src.models.models import Users, Tables


async def reserve(message: Message, state: FSMContext):
    try:
        kb = resto_list()

        await message.answer("Рады, что ты решил забронировать столик!\n"
                             "Выбери адрес ресторана, который планируешь посетить, нажав на кнопочку ниже!",
                             reply_markup=kb)
        await state.set_state(UserStates.reserve_table)
    except Exception as e:
        print("reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def reserve_address(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(address=str(message.text))

            get_data = await state.get_data()
            address = str(get_data.get('address'))
            print("address: ", address)
            markup = free_tables_list(address)

            await message.answer("Отлично, теперь выбери свободный столик!\n"
                                 "\n"
                                 "Если у тебя будут какие-либо вопросы, "
                                 "то ты можешь обязательно обратиться по команде /support!", reply_markup=markup)
            await state.set_state(UserStates.confirm_reserve_table)
    except Exception as e:
        print("reserve_address: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def confirm_reserve(message: Message, state: FSMContext):
    try:
        with app.app_context():
            tg_username = message.from_user.username

            is_user = Users.get_current(tg_username)

            if is_user:
                await state.update_data(table_name=message.text)

                get_data = await state.get_data()
                table_name = get_data.get('table_name')

                reserve_table = Tables.reserve(table_name, tg_username)

                if reserve_table is not None:
                    await message.answer(f"Отлично! {reserve_table.table_name} забронирован!\n"
                                         f"Через несколько минут с тобой свяжется Администратор ресторана,"
                                         f"чтобы подтвердить бронь!\n"
                                         f"\n"
                                         f"Увидимся :)"
                                         f"\n"
                                         f"Обязательно оставь отзыв после того, как "
                                         f"посетишь наш ресторан по команде /feedback")
                else:
                    await message.answer("К сожалению, выбранный вами стол не найден.")
    except Exception as e:
        print("confirm_reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()