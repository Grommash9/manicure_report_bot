from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Открыть смену'))
    m.insert(KeyboardButton('Закрыть смену'))
    return m


def cash_desk_is_terminal_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Да'))
    m.insert(KeyboardButton('Нет'))
    m.insert(KeyboardButton('Отмена'))
    return m


def comment_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Пропустить'))
    m.insert(KeyboardButton('Отмена'))
    return m
