from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    set_name = State()
    set_phone = State()

    reserve_table = State()
    confirm_reserve_table= State()

    feedback_text = State()
    feedback_score = State()

    change_time_reserve = State()

    menu_questions = State()
    resto_address = State()

    your_questions = State()
    user_questions = State()