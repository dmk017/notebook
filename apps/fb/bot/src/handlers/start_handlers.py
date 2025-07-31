from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.handlers.data.texts.get_texts import get_i18n_text



router = Router(name="start_router")


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(get_i18n_text('texts.start_messages.start'))

