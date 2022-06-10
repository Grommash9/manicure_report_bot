from aiogram.dispatcher.filters.state import StatesGroup, State


class Administrator(StatesGroup):
    main = State()

    class StartDay(StatesGroup):
        time = State()
        cash = State()
        comment = State()

    class EndDay(StatesGroup):
        bouquet_group_cash_desk = State()
        bouquet_group_terminal = State()
        bouquet_cosmetic_industry_cash_desk = State()
        bouquet_cosmetic_industry_terminal = State()
        cash_desk = State()
        cash_desk_is_terminal = State()
        master_comment = State()
        comment = State()
