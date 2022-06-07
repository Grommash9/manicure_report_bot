from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    main = State()

    class PhoneNumber(StatesGroup):
        phone = State()
