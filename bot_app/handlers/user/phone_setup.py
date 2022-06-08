import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot_app import db, markup, config
from bot_app.misc import bot, dp
from bot_app.state.user.base import User


@dp.message_handler(content_types=aiogram.types.ContentType.CONTACT,
                    state=User.PhoneNumber.phone)
async def get_contact(message: Message, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        await state.finish()
        await db.user.set_phone_number(message.from_user.id,
                                       message.contact.phone_number)
        for admins in config.ADMINS:
            try:
                await bot.send_message(admins,
                                       f'Запрошен доступ к боту\n\n'
                                       f'Пользователь: {message.from_user.first_name}\n'
                                       f'Юзернейм: @{message.from_user.username}\n'
                                       f'Номер телефона {message.contact.phone_number}\n',
                                       reply_markup=markup.admin_m.user_registration(message.from_user.id))
            except Exception as e:
                pass
            else:
                await bot.send_message(message.from_user.id,
                                       'Ваш номер телефона принят, администратор назначит вам роль и вы будете оповещены об этом!',
                                       reply_markup=ReplyKeyboardRemove())
                return
        return
    await bot.send_message(message.from_user.id,
                           'Можно отправлять только свой номер телефона!',
                           reply_markup=markup.user.user_m.phone_menu())
