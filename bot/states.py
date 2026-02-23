from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    MAIN = State()
    TICKETS_LIST = State()
    TICKET = State()
    NEW_TICKET = State()
    NEW_MESSAGE = State()
