import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import markup, config
from bot_app.misc import bot, dp
from bot_app.state.user.administrator import Administrator


@dp.message_handler(text='Открыть смену', state=Administrator.main)
async def client_report_getter(message: Message, state: FSMContext):
    await state.set_state(Administrator.StartDay.time)
    await bot.send_message(message.from_user.id,
                           'Введите время открытия смены: \n\n'
                           'Например 15:00',
                           reply_markup=markup.base.cancel())


@dp.message_handler(text='Отмена', state=Administrator.StartDay)
async def client_report_cancel(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state(Administrator.main)
    await bot.send_message(message.from_user.id,
                           'Отправка отчета отменена успешно',
                           reply_markup=markup.user.administrator_m.main_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.StartDay.time)
async def client_report_getter(message: Message, state: FSMContext):
    await state.set_data({'time': message.text})
    await state.set_state(Administrator.StartDay.cash)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста введите деньги в кассе на начало рабочего дня!',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.StartDay.cash)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'cash': message.text})
    await state.set_state(Administrator.StartDay.comment)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста введите комментарий!',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.StartDay.comment)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'comment': message.text})
    data = await state.get_data()
    await state.finish()
    await state.set_state(Administrator.main)
    for admins in config.ADMINS:
        try:
            await bot.send_message(admins,
                                   f"<b>Администратор @{message.from_user.username} #{message.from_user.first_name} открыл смену!</b>\n\n"
                                   f"Время открытия: {data['time']}\n"
                                   f"Деньги в кассе: {data['cash']}\n"
                                   f"Комментарий: {data['comment']}\n")
        except Exception as e:
            pass

    await bot.send_message(message.from_user.id,
                           'Отчет отправлен!',
                           reply_markup=markup.user.administrator_m.main_menu())