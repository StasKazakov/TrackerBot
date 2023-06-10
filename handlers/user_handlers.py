import asyncio
import random
import logging
from TrackerBot.config import Config, load_config
from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from TrackerBot.tools.db import Database
from TrackerBot.tools.keyboard import menu_getter, start_menu, cancel_button
from TrackerBot.tools.states import States
from TrackerBot.tools.delete import delete
from TrackerBot.redirection.url_flask import UTMTracker
from TrackerBot.main import language_data

logging.basicConfig(filename="all_log.log", level=logging.INFO, format="%(asctime)s - $(levelname)s - %(message)s")
router = Router()
config: Config = load_config()
db = Database("TrackerBot.db")

async def state_geter(strs: str) -> str:
    return strs.split(':')[1]

@router.callback_query(Text(text=['link']))   # function for state, in which user will send us the link
async def answer_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.message.text != 'Add link':
        await callback.message.edit_text(text=language_data.awaiting_the_link(db.check_language(callback.from_user.id)),
                                         reply_markup=None, show_alert=False)
    await state.set_state(States.link_waiting)

@router.message(F.text, StateFilter(States.link_waiting))     # Dania's function, in developing
async def admin_start(message: Message, state: FSMContext):
    g = ['www', '.com', 'https', '@']
    lang = db.check_language(int(message.from_user.id))
    if all([True if i in message.text else False for i in g]):
        link = message.text
        logging.info("trying to make new link")
        redirect_url = UTMTracker(link, 'Telegram', 'adv', 'new service').add_utm_params()
        await message.answer(redirect_url, parse_mode='HTML')
        await message.answer(text='Something else?', reply_markup=menu_getter(lang))
    else:
        await message.answer(language_data.incorrect_link(lang), parse_mode='HTML', reply_markup=menu_getter(lang))
    await state.clear()

@router.callback_query(Text(text=['state']))
async def answer_menu(callback: types.CallbackQuery):
    if callback.message.text != 'Statistics':
        await callback.message.edit_text(text='Statistics',
                                         reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)
    await callback.answer()

@router.callback_query(Text(text=['help']))
async def answer_menu(callback: types.CallbackQuery):
    if callback.message.text != 'Instruction':
        await callback.message.edit_text(text='Instruction',
                                         reply_markup=menu_getter(db.check_language(callback.from_user.id)), show_alert=False)
    await callback.answer()

@router.callback_query(Text(text=['call']))
async def answer_menu(callback: types.CallbackQuery, state: FSMContext):
    lang = db.check_language(callback.from_user.id)
    await callback.message.edit_text(text=language_data.instruction_for_report(lang), reply_markup=cancel_button(db.check_language(int(callback.from_user.id))))
    await state.set_state(States.call)

@router.callback_query(Text(text=['cancel']), StateFilter(States.call))
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    lang = db.check_language(callback.from_user.id)
    msg = await callback.message.answer(language_data.after_canselling(lang))
    await state.clear()
    await delete(msg, time=2)
    await callback.message.edit_text("Main Menu",
                                     reply_markup=menu_getter(lang), show_alert=False)

@router.message(F.text, StateFilter(States.link_waiting))     # Dania's function, in developing
async def state_call(message: Message, state: FSMContext, bot: Bot):
    print('here')
    lang = db.check_language(message.from_user.id)
    admin = random.choice(config.tg_bot.admin_ids)
    await bot.send_message(chat_id=admin, text=message.text)
    msg = await message.reply(language_data.answer_on_report(lang))
    await delete(msg, time=2)
    await message.answer("Main Menu",
                         reply_markup=menu_getter(lang), show_alert=False)
    await state.clear()