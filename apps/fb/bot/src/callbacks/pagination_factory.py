from aiogram.filters.callback_data import CallbackData

class PaginationCallbackFactory(CallbackData, prefix="PCF"):
    action: str
    page: int