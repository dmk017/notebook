from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import json

import redis
import logging

from .config import get_settings
from .handlers import start_handlers, search_handlers
from .middleware.auth_middlware import CheckTokenMiddleware

settings = get_settings()
redis_client = redis.Redis(host=settings.redis_connection_url, port=settings.redis_port, db=0)
bot = Bot(token=settings.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)


def listen_to_redis(stop_event):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(settings.redis_chanel_name)

    while not stop_event.is_set():
        message = pubsub.get_message(timeout=1)
        if message:
            if message['type'] == 'message':
                data = json.loads(message['data'].decode())
                user_id = data['user_id']
                logging.info(f"User {user_id} was Authorized")


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(CheckTokenMiddleware(bot=bot, redis_connection_url=settings.redis_connection_url, redis_port=settings.redis_port, redis_db=0, redis_keys_name=settings.redis_keys_name))
    dp.include_routers(start_handlers.router, search_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
