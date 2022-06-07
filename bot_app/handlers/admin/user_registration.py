import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot_app import db
from bot_app.misc import bot, dp


@dp.callback_query_handler(text_startswith='set-worker_')
async def set_worker_call(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[-1]
    await call.answer()
    await call.message.delete()
    await db.user.set_role(user_id, 1)
    try:
        await bot.send_message(user_id,
                               'Администратор рассмотрел вашу заявку и вам была установлена роль Мастер\n\n'
                               'Для начала работы введите команду /start')
    except Exception as e:
        await bot.send_message(call.from_user.id,
                               f'Роль была установлена, но оповещение не было доставлено из-за {e}')
    else:
        await bot.send_message(call.from_user.id,
                               f'Роль была установлена, оповещение было доставлено')


@dp.callback_query_handler(text_startswith='set-admin_')
async def set_admin_call(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[-1]
    await call.answer()
    await call.message.delete()
    await db.user.set_role(user_id, 2)
    try:
        await bot.send_message(user_id,
                               'Администратор рассмотрел вашу заявку и вам была установлена роль Администратор\n\n'
                               'Для начала работы введите команду /start')
    except Exception as e:
        await bot.send_message(call.from_user.id,
                               f'Роль была установлена, но оповещение не было доставлено из-за {e}')
    else:
        await bot.send_message(call.from_user.id,
                               f'Роль была установлена, оповещение было доставлено')



@dp.callback_query_handler(text_startswith='set-no_')
async def set_no_call(call: CallbackQuery, state: FSMContext):
    await call.answer('Запрос отклонен', show_alert=True)
    await call.message.delete()

