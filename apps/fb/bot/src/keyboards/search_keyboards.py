from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils import safetyCallbackKey
from src.callbacks.models_factory import ModelsCallbackFactory
from src.callbacks.properties_factory import PropertiesCallbackFactory
from src.callbacks.pagination_factory import PaginationCallbackFactory
from src.handlers.data.texts.get_texts import get_i18n_text


def get_pagination_actions(page: int, is_next: bool):
    if page == 1 and is_next == False:
        return []
    if page == 1 and is_next == True:
        return ['next']
    if page > 1 and is_next == False:
        return ['prev']
    if page > 1 and is_next == True:
        return ['prev', 'next']


def get_keyboard_models(models_data: dict, page: int=1, limit: int=10):
    builder = InlineKeyboardBuilder()

    for model in models_data['data'][(page - 1)* limit: page*limit]:
        builder.button(text=model['name'], callback_data=ModelsCallbackFactory(key=safetyCallbackKey(model['name']), id=model['_id']))
    if len(models_data) % 2 != 0:
        builder.button(text='', callback_data=ModelsCallbackFactory(key='', id='')) 
    builder.button(text=get_i18n_text('texts.keyboards.search_all_model'), callback_data=ModelsCallbackFactory(id='', key='ALL_MODELS'))
    builder.button(text=get_i18n_text('texts.keyboards.cancel_search_emoji'), callback_data=ModelsCallbackFactory(id='', key='CANCEL_SEARCH')) 
    for action in get_pagination_actions(page, models_data['count'] > page * limit):
        button_text = get_i18n_text('texts.keyboards.next_page') if action == 'next' else get_i18n_text('texts.keyboards.previous_page')
        builder.button(text=button_text, callback_data=PaginationCallbackFactory(action=action, page=page))
    builder.adjust(2)  

    return builder.as_markup()

def get_keyboard_properties(properties_data: dict):
    builder = InlineKeyboardBuilder()
    count_button = 0
    for _, propery_value in properties_data.items():
        for data_field in propery_value:
            count_button += 1
            builder.button(text=data_field['name'], callback_data=PropertiesCallbackFactory(
                key=safetyCallbackKey(data_field['name']),
                primitive_type=data_field['primitive_type'],
                is_required=data_field['is_required'],
                validation=data_field['validation']
            ))
    builder.button(text=get_i18n_text('texts.keyboards.search_everywhere'), callback_data=PropertiesCallbackFactory(
                key='SEARCH_EVERYWHERE',
                primitive_type='',
                is_required=False,
                validation=''
    ))
    count_button += 1
    if count_button % 2 != 0:
        builder.button(text="", callback_data=PropertiesCallbackFactory(
                key="",
                primitive_type='',
                is_required=False,
                validation=''
            ))
    builder.button(text=get_i18n_text('texts.keyboards.start_search_emoji'), callback_data=PropertiesCallbackFactory(
                key='START_SEARCH',
                primitive_type='',
                is_required=False,
                validation=''

    ))
    builder.button(text=get_i18n_text('texts.keyboards.cancel_search_emoji'), callback_data=PropertiesCallbackFactory(
                key='CANCEL_SEARCH',
                primitive_type='',
                is_required=False,
                validation=''
    ))

    builder.adjust(2)
    return builder.as_markup()
