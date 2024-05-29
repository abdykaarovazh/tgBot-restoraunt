from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app
from project.backend.src.telegram.keyboard.reply.reply import support_questions
from project.backend.src.telegram.states import UserStates
from project.backend.src.models.models import Tables
from project.backend.src.telegram.keyboard.reply.reply import resto_list, reserved_tables_by_user
from project.backend.src.telegram.bot import logger

# Обработка команды /support
async def support(message: Message, state: FSMContext):
    try:
        await message.answer("Произошли какие-то проблемы? Выберите вопрос из списка ниже:",
                             reply_markup=support_questions())

        if message.text == 'Сменить время бронирования':
            await state.set_state(UserStates.change_time_reserve)
        elif message.text == 'Вопрос по Меню':
            await state.set_state(UserStates.menu_questions)
        elif message.text == 'Свой вопрос':
            await state.set_state(UserStates.your_questions)
        elif message.text == 'Отменить бронь':
            await state.set_state(UserStates.quit_table)
        else:
            await state.clear()
    except Exception as e:
        logger.exception("support: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


# Обработка варианта в выборе "Сменить время бронирования"
async def change_time(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(change=message.text)

            tables = Tables.get_all(message.from_user.username, 'Y')

            if tables:
                for table in tables:
                    await message.answer("У вас забронированы следующие столы:\n"
                                         f"<b>{table.table_name}</b>\n"
                                         f"<b>Адрес</b>: {table.address}\n"
                                         f"<b>Количество мест</b>: {table.place_count}\n"
                                         f"<b>Дата и время бронирования</b>: {table.time_reserve}\n")
                    await message.answer("Выберите, столик, у которого хотели бы сменить дату и/или время посещение",
                                         reply_markup=reserved_tables_by_user(message.from_user.username))
                await state.set_state(UserStates.vote_table_before_change_time)
            else:
                await message.answer(
                    'Вы ещё не бронировали ни одного столика!\n'
                    'Вы сможете сделать это через команду /reserve'
                )
    except Exception as e:
        logger.exception("support_change: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы...."
        )

async def vote_table_before_change_time(message: Message, state: FSMContext):
    try:
        await state.update_data(user_table=message.text)

        await message.answer("Хорошо, укажите, пожалуйста, новое дату и/или "
                             "время посещения ниже в формате: <b>21.05.2024 16:00</b>")
        await state.set_state(UserStates.change_date_time)
    except Exception as e:
        logger.exception("vote_table_before_change_time: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы...."
        )

async def change_date_time(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(date_time=message.text)
            get_data = await state.get_data()
            user_table = get_data.get('user_table')
            date_time = get_data.get('date_time')
            table = user_table[:9]                   # Берем только необходимое название стола без адреса
            date = date_time[:10]                    # Берем только дату из сообщения
            time = date_time[11:]                    # Берем только время из сообщения

            Tables.change_date_time(message.from_user.username, table, date, time)
            await message.answer("Дата и время успешно обновлены!\n"
                                 "Новые данные по изменённому столику:\n"
                                 f"{table}\n"
                                 f"Дата и время: {date} {time}")
    except Exception as e:
        logger.exception("change_date_time: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы...."
        )
    finally:
        await state.clear()


# Обработка варианта в выборе "Свой вопрос"
async def menu_questions(message: Message, state: FSMContext):
    try:
        await state.update_data(menu_question=message.text)

        markup = resto_list()
        await message.answer('Выберите, пожалуйста, адрес ресторана,'
                             'по меню которого у Вас вопрос', reply_markup=markup)
        await state.set_state(UserStates.resto_address)
    except Exception as e:
        logger.exception("menu_questions: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

# Переход состояния после выбора адреса ресторана
async def resto_addresses(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)

        get_data = await state.get_data()
        address = get_data.get('address')

        await message.answer(f'Отлично, с Вами свяжется Администратор ресторана по адресу {address}!\n'
                             f'Если произойдёт что-то ещё обязательно пишите, мы всегда на связи!')
    except Exception as e:
        logger.exception("resto_addresses: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()


# Обработка варианта в выборе "Вопрос по Меню"
async def self_questions(message: Message, state: FSMContext):
    try:
        await state.update_data(question=message.text)

        await message.answer("Хорошо, напишите, пожалуйста, свой вопрос в нашу тех. поддержку @suncorner_support "
                             "и мы обязательно тебе поможем!")
    except Exception as e:
        logger.exception("self_questions: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()


# Обработка варианта в выборе "Отменить бронь"
async def quit_reserve(message: Message, state: FSMContext):
    try:
        with app.app_context():
            tables = Tables.get_all(message.from_user.username, 'Y')
            for table in tables:
                await message.answer("У вас забронированы следующие столы:\n"
                                     f"<b>{table.table_name}</b>\n"
                                     f"<b>Адрес</b>: {table.address}\n"
                                     f"<b>Количество мест</b>: {table.place_count}\n"
                                     f"<b>Дата и время бронирования</b>: {table.time_reserve}\n")
            await message.answer("Если Вы уверены, что хотите отменить бронь, выберите, пожалуйста, "
                                 "столик, бронь которого хотели бы отменить",
                                 reply_markup=reserved_tables_by_user(message.from_user.username))
            await state.set_state(UserStates.confirm_quit)
    except Exception as e:
        logger.exception("quit_reserve: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def confirm_quit(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(user_table=message.text)
            get_data = await state.get_data()
            user_table = get_data.get('user_table')
            table = user_table[:9]   # Берем только необходимое название стола без адреса

            table = Tables.unreserve(message.from_user.username, table)
            print(table)
            await message.answer(f"Бронь {user_table} успешно отмена!\n"
                                 f"Очень жаль, конечно, но если Вы передумаете, "
                                 f"то Вы сможете сделать это команде /reserve\n"
                                 f"Успехов Вам!")
    except Exception as e:
        logger.exception("confirm_quit: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()
