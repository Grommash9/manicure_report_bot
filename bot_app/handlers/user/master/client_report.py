import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import db, markup, config
from bot_app.misc import bot, dp
from bot_app.state.user.master import Master


@dp.message_handler(text='Отчёт по клиенту', state=Master.main)
async def client_report_getter(message: Message, state: FSMContext):
    await state.set_state(Master.ClientReport.photo)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста отправьте фото с описанием, оно будет доставлено администрации: ',
                           reply_markup=markup.base.cancel())


@dp.message_handler(text='Отмена', state=Master.ClientReport.photo)
async def client_report_cancel(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state(Master.main)
    await bot.send_message(message.from_user.id,
                           'Отправка отчета отменена успешно',
                           reply_markup=markup.user.master_m.main_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.PHOTO, state=Master.ClientReport.photo)
async def client_report_getter(message: Message, state: FSMContext):
    if message.caption is None:
        await bot.send_message(message.from_user.id,
                               'Пожалуйста укажите описание к фото и попробуйте снова!',
                               reply_markup=markup.base.cancel())
        return
    await state.finish()
    await state.set_state(Master.main)
    admin_list = await db.user.get_all_admins()
    for admin in admin_list:
        try:
            await bot.send_photo(admin,
                                 photo=message.photo[-1].file_id,
                                 caption=f"<b>Отчет по клиенту от @{message.from_user.username} {message.from_user.first_name}</b>\n\n"
                                         f"{message.caption}\n\n"
                                         f"Создано: {message.date}")
        except Exception as e:
            pass

    for admin in config.ADMINS:
        try:
            await bot.send_photo(admin,
                                 photo=message.photo[-1].file_id,
                                 caption=f"<b>Отчет по клиенту от @{message.from_user.username} {message.from_user.first_name}</b>\n\n"
                                         f"{message.caption}\n\n"
                                         f"Создано: {message.date}")
        except Exception as e:
            pass

    await bot.send_message(message.from_user.id,
                           'Отчет успешно отправлен',
                           reply_markup=markup.user.master_m.main_menu())
