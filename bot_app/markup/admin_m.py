from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_registration(user_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.insert(InlineKeyboardButton('Работник', callback_data=f'set-worker_{user_id}'))
    m.insert(InlineKeyboardButton('Администратор', callback_data=f'set-admin_{user_id}'))
    m.insert(InlineKeyboardButton('Отклонить', callback_data=f'set-no_{user_id}'))
    return m
