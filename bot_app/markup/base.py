from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Отмена'))
    return m

