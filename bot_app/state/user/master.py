from aiogram.dispatcher.filters.state import StatesGroup, State


class Master(StatesGroup):
    main = State()

    class ClientReport(StatesGroup):
        photo = State()

    class EndDayReport(StatesGroup):
        time = State()
        photo = State()