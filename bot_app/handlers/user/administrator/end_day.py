import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import markup, config
from bot_app.misc import bot, dp
from bot_app.state.user.administrator import Administrator


@dp.message_handler(text='Закрыть смену', state=Administrator.main)
async def client_report_getter(message: Message, state: FSMContext):
    await state.set_state(Administrator.EndDay.bouquet_group_cash_desk)
    await bot.send_message(message.from_user.id,
                           'Введите суточный рапорт кассы Bouquet Group: \n\n',
                           reply_markup=markup.base.cancel())


@dp.message_handler(text='Отмена', state=Administrator.EndDay)
async def client_report_cancel(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state(Administrator.main)
    await bot.send_message(message.from_user.id,
                           'Отправка отчета отменена успешно',
                           reply_markup=markup.user.administrator_m.main_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.EndDay.bouquet_group_cash_desk)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'bouquet_group_cash_desk': message.text})
    await state.set_state(Administrator.EndDay.bouquet_group_terminal)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста введите суточный рапорт терминала Bouquet Group!',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.EndDay.bouquet_group_terminal)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'bouquet_group_terminal': message.text})
    await state.set_state(Administrator.EndDay.bouquet_cosmetic_industry_cash_desk)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста введите суточный рапорт кассы Cosmetic Industry !',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT,
                    state=Administrator.EndDay.bouquet_cosmetic_industry_cash_desk)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'bouquet_cosmetic_industry_cash_desk': message.text})
    await state.set_state(Administrator.EndDay.bouquet_cosmetic_industry_terminal)
    await bot.send_message(message.from_user.id,
                           'Пожалуйста введите суточный рапорт терминала Cosmetic Industry  !',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT,
                    state=Administrator.EndDay.bouquet_cosmetic_industry_terminal)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'bouquet_cosmetic_industry_terminal': message.text})
    await state.set_state(Administrator.EndDay.cash_desk)
    await bot.send_message(message.from_user.id,
                           'Сколько наличных в кассе?',
                           reply_markup=markup.base.cancel())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT,
                    state=Administrator.EndDay.cash_desk)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'cash_desk': message.text})
    await state.set_state(Administrator.EndDay.cash_desk_is_terminal)
    await bot.send_message(message.from_user.id,
                           'Сходится ли рапорт с системою?',
                           reply_markup=markup.user.administrator_m.cash_desk_is_terminal_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.EndDay.cash_desk_is_terminal)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'cash_desk_is_terminal': message.text})
    await state.set_state(Administrator.EndDay.master_comment)
    await bot.send_message(message.from_user.id,
                           'Напишите оценку качества мастеров ( Замечания )',
                           reply_markup=markup.user.administrator_m.comment_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.EndDay.master_comment)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'master_comment': message.text})
    await state.set_state(Administrator.EndDay.comment)
    await bot.send_message(message.from_user.id,
                           'Введите коментарий: ',
                           reply_markup=markup.user.administrator_m.comment_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.TEXT, state=Administrator.EndDay.comment)
async def client_report_getter(message: Message, state: FSMContext):
    await state.update_data({'comment': message.text})
    data = await state.get_data()
    await state.finish()
    await state.set_state(Administrator.main)
    for admins in config.ADMINS:
        try:
            await bot.send_message(admins,
                                   f'<b>Администратор @{message.from_user.username} #{message.from_user.first_name} отправил отчет!</b>\n'
                                   f'Суточный рапорт кассы Bouquet Group: \n<b>{data["bouquet_group_cash_desk"]}</b>\n'
                                   f'Суточный рапорт терминала Bouquet Group: \n<b>{data["bouquet_group_terminal"]}</b>\n'
                                   f'Суточный рапорт кассы Cosmetic Industry: \n<b>{data["bouquet_cosmetic_industry_cash_desk"]}</b>\n'
                                   f'Суточный рапорт терминала Cosmetic Industry: \n<b>{data["bouquet_cosmetic_industry_terminal"]}</b>\n'
                                   f'Сколько наличных в кассе: \n<b>{data["cash_desk"]}</b>\n'
                                   f'Сходится ли рапорт с системой: \n<b>{data["cash_desk_is_terminal"]}</b>\n'
                                   f'Оценка качества мастеров ( Замечания ): \n{data["master_comment"]}\n'
                                   f'Комментарий: \n{data["comment"]}\n\n')
        except Exception as e:
            pass

    await bot.send_message(message.from_user.id,
                           f'Отчет успешно отправлен!',
                           reply_markup=markup.user.administrator_m.main_menu())
