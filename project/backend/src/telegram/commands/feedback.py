from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from project.backend.src.telegram.states import UserStates
from project.backend.src.telegram.keyboard.reply.reply import feedback_scores

from project.backend.src.db.db_app import app

from project.backend.src.models.feedback import insert_feedback
from project.backend.src.models.models import Users


async def feedback(message: Message, state: FSMContext):
    try:
        await message.answer("Ну как тебе у нас?\n"
                             "Надеемся тебе всё понравилось! Напиши свой отзыв")
        await state.set_state(UserStates.feedback_text)
    except Exception as e:
        print("feedback: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def write_feedback(message: Message, state: FSMContext):
    try:
        kb = feedback_scores()
        await state.update_data(text=message.text)

        await message.answer("Интересное мнение, спасибо тебе за него!\n"
                             "Мы обязательно его учтём и примем во внимание!\n"
                             "\n"
                             "А теперь поставь нам оценку ниже!", reply_markup=kb)
        await state.set_state(UserStates.feedback_score)
    except Exception as e:
        print("write_feedback: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")


async def write_score(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(score=message.text)

            get_data = await state.get_data()
            feedback_text = get_data.get('text')
            feedback_score = get_data.get('score')

            user = Users.get_current(message.from_user.username)

            insert_feedback(user.user_name, feedback_text, feedback_score)

            await message.answer("Отлично! Спасибо тебе большое за то, что решил(а) поделиться своими впечатлениями.\n"
                                 "Для нас это очень важно, чтобы улучшать наши заведения!")
            await state.clear()
    except Exception as e:
        print("write_score: ", e)
        await message.answer("Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()
