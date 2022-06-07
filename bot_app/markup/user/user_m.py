from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def phone_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Отправить контакт', request_contact=True))
    return m

