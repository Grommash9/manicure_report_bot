from asyncio import get_event_loop

import aioredis
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot_app.config import TOKEN, REDIS

loop = get_event_loop()
bot = Bot(TOKEN, parse_mode='HTML', loop=loop)
storage = RedisStorage2(**REDIS, loop=loop)
dp = Dispatcher(bot, loop, storage)
redis = aioredis.Redis(decode_responses=True)
