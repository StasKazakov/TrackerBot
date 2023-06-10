from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):  # Finite state machine
    call = State()
    name_of_link = State()
    link_awaiting = State()