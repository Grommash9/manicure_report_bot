from aiogram.types import User

from bot_app.db.base import create_dict_con, create_con


def user_name_formatter(user_data: User):
    if user_data.username:
        return f"@{user_data.username}"
    return None


async def create(from_user: User):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into user (user_id, first_name, user_name) '
                      'values (%s, %s, %s)',
                      (from_user.id, from_user.first_name, user_name_formatter(from_user),))
    await con.commit()
    await cur.execute('select * from user where user_id = %s', (from_user.id,))
    user = await cur.fetchone()
    await con.ensure_closed()
    return user


async def set_phone_number(user_id, phone_number):
    con, cur = await create_dict_con()
    await cur.execute('update user set phone_number = %s where user_id = %s', (phone_number, user_id,))
    user = await cur.fetchone()
    await con.ensure_closed()
    return user


async def get(user_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from user where user_id = %s', (user_id,))
    user = await cur.fetchone()
    await con.ensure_closed()
    return user


async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from user ')
    users = await cur.fetchall()
    await con.ensure_closed()
    return users


async def set_role(user_id, role):
    con, cur = await create_dict_con()
    await cur.execute('update user set role = %s where user_id = %s', (role, user_id,))
    await con.commit()
    await con.ensure_closed()


async def get_all_admins():
    con, cur = await create_dict_con()
    await cur.execute('select * from user where role = 2')
    users = await cur.fetchall()
    await con.ensure_closed()
    return users
