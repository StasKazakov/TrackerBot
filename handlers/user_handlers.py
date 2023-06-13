import logging
import random

import uuid

from config import Config, load_config
from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import StatesGroup, State
from url_flask import UTMTracker
from tools.keyboard import menu_getter, start_menu, cancel_button, back_button
from tools.db import Database
from tools.states import States
from tools.delete import delete
from main import language_data
from config import Config, load_config

router = Router()
config: Config = load_config()
db = Database()


async def state_geter(strs: str) -> str:
    return strs.split(':')[1]

@router.callback_query(Text(text=['link']))
async def link_buttton(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(callback.from_user.id, text=language_data.resourse_name(await db.check_language(str(callback.from_user.id))))
    await callback.answer()
    await state.set_state(States.name_of_link)

@router.message(StateFilter(States.name_of_link))
async def state_link_name(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(language_data.link_awaiting(await db.check_language(str(message.from_user.id))))
    await state.update_data(name_of_link = message.text)
    await state.set_state(States.link_awaiting)

@router.message(StateFilter(States.link_awaiting))  # This function will get the link, prepare, and send to user
async def link_awaiting(message: types.Message, state: FSMContext, bot: Bot):
    logging.info('trying to convert link')
    lang = await db.check_language(str(message.from_user.id))
    link_name = await state.get_data()
    g = ['www', 'https', '://']
    redirect_url = ""
    if all([True if i in message.text else False for i in g]):
        link = message.text
        user_id = message.from_user.id
        link_id = str(uuid.uuid4())
        await db.save_user_link(str(user_id), link, link_id, link_name['name_of_link'])
        redirect_url = UTMTracker(link_id).add_utm_params()
        await message.answer(f'{language_data.link_getter(lang)}\n {redirect_url}' ) 
    else:
        await message.answer(language_data.wrong_link(lang))
    await state.clear()

@router.callback_query(Text(text=['state']))
async def statistics_button(callback: types.CallbackQuery):
    lang = await db.check_language(str(callback.from_user.id))
    links = await db.get_names_link(str(callback.from_user.id))
    if bool(links) == False:
        await callback.message.edit_text(text=language_data.statisics_without_link(lang), reply_markup=back_button(lang))
    else: 
        pass

@router.callback_query(Text(text=['back']))
async def back(callback: types.CallbackQuery, state: FSMContext):
    lang = await db.check_language(str(callback.from_user.id))
    await callback.message.edit_text(text= language_data.menu(lang), reply_markup= menu_getter(lang))

@router.callback_query(Text(text=['help']))
async def help_button(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer(text='In developing', show_alert=False)

@router.callback_query(Text(text=['call']))
async def contact_button(callback: types.CallbackQuery, state: FSMContext):
    lang = await db.check_language(str(callback.from_user.id))
    await callback.message.edit_text(text=language_data.contacts(lang), reply_markup=cancel_button(lang))
    await state.set_state(States.call)

@router.callback_query(Text(text=['cancel']), StateFilter(States.call))
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    msg = await callback.message.answer("Ok, you will be return to main menu")
    await delete(msg, time=3)
    await callback.message.edit_text("Main Menu",
                                     reply_markup=menu_getter(await db.check_language(str(callback.from_user.id))), show_alert=False)
    await state.clear()

@router.message(StateFilter(States.call))
async def state_call(message: types.Message, state: FSMContext, bot: Bot):
    lang = await db.check_language(str(message.from_user.id))
    admin = random.choice(config.tg_bot.admin_ids)
    report_name = f'Report #{random.randint(0, 100000)}'
    formatted_text = f'{report_name}\n{message.text}'
    await db.save_request(str(message.from_user.id), message.text, report_name)
    await bot.send_message(chat_id=admin, text=formatted_text)
    msg = await message.reply(language_data.thanks(lang))
    await delete(msg, time=3)
    await message.answer(language_data.menu(lang),
                         reply_markup=menu_getter(lang), show_alert=False)
    await state.clear()