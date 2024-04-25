from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    set_name = State()
    set_phone = State()

    reserve_table = State()

    feedback_text = State()
    feedback_score = State()