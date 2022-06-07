import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import db, markup, config
from bot_app.misc import bot, dp
from bot_app.state.user.master import Master


@dp.message_handler(text='Закрыть смену', state=Master.main)
async def user_download(message: Message, state: FSMContext):
    await state.set_state(Master.EndDayReport.time)
    await bot.send_message(message.from_user.id,
                           'Введите время закрытия смены: \n\n'
                           'Например 15:00',
                           reply_markup=markup.base.cancel())



@dp.message_handler(text='Отмена', state=Master.EndDayReport)
async def client_report_cancel(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state(Master.main)
    await bot.send_message(message.from_user.id,
                           'Отправка отчета отменена успешно',
                           reply_markup=markup.user.master_m.main_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Master.EndDayReport.time)
async def client_report_getter(message: Message, state: FSMContext):
    await state.set_data({'time': message.text})
    await state.set_state(Master.EndDayReport.photo)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста отправьте фото с описанием, оно будет доставлено администрации: ',
                           reply_markup=markup.base.cancel())



@dp.message_handler(content_types=aiogram.types.ContentType.PHOTO, state=Master.EndDayReport.photo)
async def client_report_getter(message: Message, state: FSMContext):
    if message.caption is None:
        await bot.send_message(message.from_user.id,
                               'Пожалуйста укажите описание к фото и попробуйте снова!',
                               reply_markup=markup.base.cancel())
        return
    data = await state.get_data()
    await state.finish()
    await state.set_state(Master.main)
    admin_list: list = await db.user.get_all_admins()
    admin_list.extend(config.ADMINS)
    for admin in admin_list:
        try:
            await bot.send_photo(admin,
                                 photo=message.photo[-1].file_id,
                                 caption=f"<b>Закрытие смены</b>\n\n"
                                         f"{message.caption}\n\n"
                                         f"Смена закрыта в: {data['time']}",
                                 )
        except Exception as e:
            pass

    await bot.send_message(message.from_user.id,
                           'Отчет успешно отправлен',
                           reply_markup=markup.user.master_m.main_menu())

