from aiogram.filters.callback_data import CallbackData
from pydantic import Field

class PropertiesCallbackFactory(CallbackData, prefix="FP"):
    primitive_type: str
    is_required: bool
    validation: str
    key: str = Field(default="PROPERTY")