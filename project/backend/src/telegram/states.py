from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    set_name = State()
    set_phone = State()

    reserve_table = State()
    set_time = State()
    set_table = State()
    confirm_reserve_table= State()

    feedback_text = State()
    feedback_score = State()

    change_time_reserve = State()

    menu_questions = State()
    resto_address = State()

    your_questions = State()
    vote_table_before_change_time = State()
    change_date_time = State()
    user_questions = State()
    quit_table = State()
    confirm_quit = State()