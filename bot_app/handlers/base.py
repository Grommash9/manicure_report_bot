from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType
from bot_app.misc import bot, dp
from bot_app import db, markup, config
from bot_app.state.user.base import User
from bot_app.state.user.master import Master
from bot_app.state.user.administrator import Administrator


@dp.message_handler(chat_type=ChatType.PRIVATE, commands=['start'], state='*')
async def process_start(message: Message, state: FSMContext):
    user_data = await db.user.create(message.from_user)
    if message.from_user.id in config.ADMINS:
        await bot.send_message(message.from_user.id,
                               'Вы авторизованы в боте как администратор, вам будут приходить заявки!')
        return
    if user_data['role'] == 0:
        await state.set_state(User.PhoneNumber.phone)
        await bot.send_message(message.from_user.id,
                               'Вам нужно авторизоваться в боте, отправьте свой номер телефона:',
                               reply_markup=markup.user.user_m.phone_menu())
        return
    if user_data['role'] == 1:
        await state.set_state(Master.main)
        await bot.send_message(message.from_user.id,
                               'Вы в меню мастера',
                               reply_markup=markup.user.master_m.main_menu())
        return
    if user_data['role'] == 2:
        await state.set_state(Administrator.main)
        await bot.send_message(message.from_user.id,
                               'Вы в меню администратора',
                               reply_markup=markup.user.administrator_m.main_menu())
        return


