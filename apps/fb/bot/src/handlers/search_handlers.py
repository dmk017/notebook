from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html
from aiogram.fsm.context import FSMContext
from typing import Dict, Any

import requests
from sys import maxsize

from .data.requests_search import create_request_body_search, create_request_body_text_search, build_request_headers
from src.keyboards.search_keyboards import get_keyboard_models, get_keyboard_properties
from src.callbacks.models_factory import ModelsCallbackFactory
from src.callbacks.properties_factory import PropertiesCallbackFactory
from src.callbacks.pagination_factory import PaginationCallbackFactory
from .data.states import SearchState
from .data.text_function import text_preparation_for_display, get_found_info
from src.config import get_settings

from src.handlers.data.texts.get_texts import get_i18n_text

settings = get_settings()
router = Router(name="search_router")


@router.message(Command('start_search'))
async def start_search(msg: Message, state: FSMContext, access_token: str):
    try:
       await state.clear()
       url_get_all_models = "{0}/models/list?page={1}&limit={2}".format(settings.url_api, 1, maxsize)
       response = requests.post(url_get_all_models, headers=build_request_headers(access_token), json={})
       if response.status_code != 200:
          await msg.reply(get_i18n_text('texts.errors.server_error'))
          return
       models = response.json()
       await msg.answer(get_i18n_text('texts.search.choosing_model'), reply_markup=get_keyboard_models(models, page=1, limit=6))
       await state.update_data(all_models_data=models)
       await state.set_state(SearchState.choosing_model)

    except Exception as e:
        await msg.reply(get_i18n_text('texts.errors.server_error') + str(e))
   
@router.callback_query(SearchState.choosing_model, PaginationCallbackFactory.filter())
async def callbacks_paginations(callback: types.CallbackQuery, callback_data: PaginationCallbackFactory, state: FSMContext):
    try:
        state_data = await state.get_data()
        new_page = int(callback_data.page) + 1 if callback_data.action == 'next' else int(callback_data.page) - 1
        await callback.message.edit_text(get_i18n_text('texts.search.choosing_model'), reply_markup=get_keyboard_models(state_data['all_models_data'], page=new_page, limit=6))
    except Exception as e:
        await callback.message.answer(get_i18n_text('texts.errors.server_error') + str(e))

@router.callback_query(SearchState.choosing_model, ModelsCallbackFactory.filter())
async def callbacks_choosing_model(callback: types.CallbackQuery, callback_data: ModelsCallbackFactory, state: FSMContext, access_token: str):
    try:
        selected_model_name, selected_model_id = callback_data.key, callback_data.id
        if callback_data.key == 'CANCEL_SEARCH':
            await state.clear()
            await callback.message.answer(get_i18n_text('texts.search.return_to_search'))
            await callback.answer('')
            return
        await state.update_data(model_id=selected_model_id, selected_model_name=selected_model_name)
        if callback_data.key == 'ALL_MODELS':
            await state.set_state(SearchState.search_by_text)
            await callback.message.answer(get_i18n_text('texts.search.input_filter'))
            await callback.answer('')
            return
        await callback.answer(text=get_i18n_text('texts.search.seting_filter') + selected_model_name, show_alert=True)
        waiting_msg = await callback.message.answer(get_i18n_text('texts.search.waiting'))

        selected_model_data = requests.get(url="{0}/models/{1}".format(settings.url_api, selected_model_id), headers=build_request_headers(access_token))
        if selected_model_data.status_code != 200:
            await callback.message.answer(get_i18n_text('texts.errors.server_error'))
            return
        properties_id = [property['payload']['_id'] for property in selected_model_data.json()['properties']]
        properties_info = []
        for id_property in properties_id:
            property_data = requests.get(url="{0}/properties/{1}".format(settings.url_api, id_property), headers=build_request_headers(access_token))
            if property_data.status_code != 200:
                await callback.message.answer(get_i18n_text('texts.errors.server_error'))
                return
            properties_info.append(property_data.json())
                
        properties_info = {poperty['name']: poperty['properties'] for poperty in properties_info}
        await state.update_data(properties=properties_info)
        await waiting_msg.delete()
        await callback.message.answer(text=get_i18n_text('texts.search.input_parameters') + html.bold(html.quote(selected_model_name)), reply_markup=get_keyboard_properties(properties_info))
        await state.update_data(search_info={})
        await state.set_state(SearchState.choosing_parameters)

    except Exception as e:
        await callback.message.answer(get_i18n_text('texts.errors.server_error') + str(e))


@router.message(SearchState.choosing_model)
async def callbacks_choosing_model_incorrectly(msg: Message):
    """ Хендлер отлавливает неверный шаг пользователя"""

    await msg.reply(get_i18n_text('texts.search.wrong_move'))

@router.message(SearchState.search_by_text)
async def search_by_text(msg: Message, state: FSMContext, access_token: str):
    try:
        waiting_msg = await msg.answer(get_i18n_text('texts.search.waiting'))
        data_state = await state.get_data()
        url = "{0}/objects/search".format(settings.url_api)
        response = requests.post(url, json=create_request_body_text_search(msg.text, data_state['model_id']), headers=build_request_headers(access_token))
        if response.status_code != 200:
            raise Exception(get_i18n_text('texts.errors.server_error'))
        json_response = response.json()
        await waiting_msg.delete()
        await msg.answer(get_found_info(json_response))
        await state.clear()
        
    except Exception as e:
        await msg.reply(get_i18n_text('texts.errors.server_error') + str(e))



@router.callback_query(SearchState.choosing_parameters, PropertiesCallbackFactory.filter())
async def callbacks_choosing_parameters(callback: types.CallbackQuery, callback_data: PropertiesCallbackFactory, state: FSMContext, access_token: str):
    try:
        match callback_data.key:
            case 'CANCEL_SEARCH':
                await state.clear()
                await callback.message.answer(get_i18n_text('texts.search.return_to_search'))
                await callback.answer('')
                return
            case 'SEARCH_EVERYWHERE':
                await state.set_state(SearchState.search_by_text)
                data_state = await state.get_data()
                await callback.message.answer(get_i18n_text('texts.search.input_filter_field') + html.bold(data_state["selected_model_name"]) + get_i18n_text('texts.search.clarification'))
                await callback.answer('')
                return
            case 'START_SEARCH':
                waiting_msg = await callback.message.answer(get_i18n_text('texts.search.waiting'))
                await callback.answer()
                data_for_search = await state.get_data()
                url = "{0}/objects/search".format(settings.url_api)
                response = requests.post(url, json=create_request_body_search(data_for_search), headers=build_request_headers(access_token))
                if response.status_code != 200:
                    await callback.message.answer(get_i18n_text('texts.errors.server_error') + get_i18n_text('texts.search.return_to_search'))
                    await state.clear()
                    return
                json_response = response.json()
                await waiting_msg.delete()
                await callback.message.answer(get_found_info(json_response))
                await state.clear()
            case _:
                await state.update_data(curent_data_field_name=callback_data.key)
                await callback.answer(text=get_i18n_text('texts.search.set_field') + callback_data.key + get_i18n_text('texts.search.input_field_value'), show_alert=True)
                await state.set_state(SearchState.input_parameter_value)

    except Exception as e:
        await callback.message.answer(get_i18n_text('texts.errors.server_error') + str(e))
    
@router.message(SearchState.choosing_parameters)
async def callbacks_choosing_parameters_incorrectly(msg: Message):
    """ Хендлер отлавливает неверный шаг пользователя"""

    await msg.reply(get_i18n_text('texts.search.wrong_move'))


@router.message(SearchState.input_parameter_value)
async def input_param_value(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        data_field = data['curent_data_field_name']
        data['search_info'][data_field] = msg.text
        update_search_info = data['search_info']
        await state.update_data(search_info=update_search_info)
        await state.set_state(SearchState.choosing_parameters)
        properties_info = data['properties']
        await msg.reply(get_i18n_text('texts.search.completed_fields') + text_preparation_for_display(update_search_info) + get_i18n_text('texts.search.continue_filling') + html.bold(html.quote(data['selected_model_name'])) + get_i18n_text('texts.search.or_start_search'), reply_markup=get_keyboard_properties(properties_info))
    except Exception as e:
        await msg.reply(get_i18n_text('texts.errors.server_error') + str(e))
