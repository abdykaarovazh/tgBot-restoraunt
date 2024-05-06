from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.db.db_app import app
from project.backend.src.telegram.keyboard.reply.reply import support_questions
from project.backend.src.telegram.states import UserStates
from project.backend.src.models.models import Tables
from project.backend.src.telegram.keyboard.reply.reply import resto_list


async def support(message: Message, state: FSMContext):
    try:
        markup = support_questions()
        await message.answer("Произошли какие-то проблемы? Выберите вопрос из списка ниже:", reply_markup=markup)

        if message.text == 'Сменить время бронирования':
            await state.set_state(UserStates.change_time_reserve)
        elif message.text == 'Вопрос по Меню':
            await state.set_state(UserStates.menu_questions)
        elif message.text == 'Свой вопрос':
            await state.set_state(UserStates.your_questions)
        else:
            await state.clear()

    except Exception as e:
        print("support: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def change_time(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(change=message.text)
            tg_username = message.from_user.username

            is_table = Tables.query.filter_by(user_name=tg_username, is_reserve='Y').first()

            if is_table:
                await message.answer('Захотел сменить время своего забронированного столика?\n'
                                     'Хорошо, напиши ниже время, которое тебе удобно и Администратор свяжется с тобой!')
            else:
                await message.answer('Ты ещё не бронировал(а) ни одного столика!\n'
                                     'Ты сможешь сделать это через команду /reserve')
    except Exception as e:
        print("support_change: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()


async def menu_questions(message: Message, state: FSMContext):
    try:
        await state.update_data(menu_question=message.text)

        markup = resto_list()
        await message.answer('Выберите, пожалуйста, адрес ресторана,'
                             'по меню которого у Вас вопрос', reply_markup=markup)
        await state.set_state(UserStates.resto_address)
    except Exception as e:
        print("menu_questions: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")

async def resto_addresses(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)

        get_data = await state.get_data()
        address = get_data.get('address')

        await message.answer(f'Отлично, с тобой свяжется Администратор ресторана по адресу {address}!\n'
                             f'Если произойдёт что-то ещё обязательно пиши, мы всегда на связи!')
    except Exception as e:
        print("resto_addresses: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()


async def self_questions(message: Message, state: FSMContext):
    try:
        await state.update_data(question=message.text)

        await message.answer("Хорошо, напиши свой вопрос в нашу тех. поддержку @suncorner_support "
                             "и мы обязательно тебе поможем!")
    except Exception as e:
        print("self_questions: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()