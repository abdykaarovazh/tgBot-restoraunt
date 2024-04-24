from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app

from project.backend.src.telegram.states import UserStates
from project.backend.src.telegram.keyboard.reply.reply import free_tables_list

from project.backend.src.models.tables import tables_collection
from project.backend.src.models.models import Users


async def reserve(message: Message, state: FSMContext):
    kb = free_tables_list()

    await message.answer("Рады, что ты решил забронировать столик!\n"
                         "Выбери один из свободных столиков нажав на кнопочку ниже!", reply_markup=kb)
    await state.set_state(UserStates.reserve_table)


async def confirm_reserve(message: Message, state: FSMContext):
    with app.app_context():
        tg_username = message.from_user.username

        is_user = Users.get_current(tg_username)

        if is_user:
            await state.update_data(table_name=message.text)

            get_data = await state.get_data()
            table_name = get_data.get('table_name')

            tables_collection.reserve_table(table_name)

            await message.answer(f"Отлично! {table_name} забронирован!\n"
                                 f"Через несколько минут с тобой свяжется Администратор ресторана,"
                                 f"чтобы подтвердить бронь!\n"
                                 f"\n"
                                 f"Увидимся :)"
                                 f"\n"
                                 f"Обязательно оставь отзыв после того как посетишь наш ресторан.\n"
                                 f"Ты сможешь сделать это по команде /feedback")