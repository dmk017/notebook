from typing import Optional
from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class ModelsCallbackFactory(CallbackData, prefix="FM"):
    id: str
    key: str = Field(default="MODEL")