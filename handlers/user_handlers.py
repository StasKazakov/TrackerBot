import asyncio
import random

import uuid

from config import Config, load_config
from aiogram import Router, types
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from run import db
from url_flask import UTMTracker
from tools.db import Database
from tools.keyboard import menu_getter, start_menu, cancel_button
from tools.states import States
from tools.delete import delete
from main import language_data

router = Router()
config: Config = load_config()

async def state_geter(strs: str) -> str:
    return strs.split(':')[1]

@router.callback_query(Text(text=['link']))
async def answer_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(callback.from_user.id, text=language_data.resourse_name(await db.check_language(str(callback.from_user.id))))
    await callback.answer()
    await state.set_state(States.name_of_link)

@router.message(StateFilter(States.name_of_link))
async def answer_menu(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(language_data.link_awaiting(await db.check_language(str(message.from_user.id))))
    await state.set_state(States.link_awaiting)

@router.message(StateFilter(States.link_awaiting))  # This function will get the link, prepare, and send to user
async def answer_menu(message: types.Message, state: FSMContext, bot: Bot):
    lang = await db.check_language(str(message.from_user.id))

    g = ['www', 'https', '://']
    redirect_url = ""
    if all([True if i in message.text else False for i in g]):
        link = message.text
        user_id = message.from_user.id
        link_id = str(uuid.uuid4())
        await db.save_user_link(str(user_id), link, link_id)
        redirect_url = UTMTracker(link_id).add_utm_params()
        await message.answer(redirect_url) # here must be READY LINK
    await state.clear()

@router.callback_query(Text(text=['state']))
async def answer_menu(callback: types.CallbackQuery):
    await callback.answer(text='In developing', show_alert=False)

@router.callback_query(Text(text=['help']))
async def answer_menu(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer(text='In developing', show_alert=False)

@router.callback_query(Text(text=['call']))
async def answer_menu(callback: types.CallbackQuery, state: FSMContext):
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
    formatted_text = f'Report #{random.randint(0, 100000)}\n{message.text}'
    await bot.send_message(chat_id=admin, text=formatted_text)
    msg = await message.reply(language_data.thanks(lang))
    await delete(msg, time=3)
    await message.answer(language_data.menu(lang),
                         reply_markup=menu_getter(lang), show_alert=False)
    await state.clear()