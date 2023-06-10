from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):  # Finite state machine
    call = State()
    link_waiting = State()