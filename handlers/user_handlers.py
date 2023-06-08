import asyncio
import random
from config import Config, load_config
from aiogram import Router, types
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from tools.db import Database
from tools.keyboard import menu_getter, start_menu, cancel_button
from tools.states import States
from tools.delete import delete

router = Router()
config: Config = load_config()
db = Database(config.db.host, config.db.user, config.db.password, config.db.database)

async def state_geter(strs: str) -> str:
    return strs.split(':')[1]

@router.callback_query(Text(text=['link']))
async def answer_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.message.text != 'Add link':
        await callback.message.edit_text(text='Add link',
                                         reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)
    await callback.answer()

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
                                         reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)
    await callback.answer()

@router.callback_query(Text(text=['call']))
async def answer_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Ok, send your request below', reply_markup= cancel_button(db.check_language(int(callback.from_user.id))))
    await state.set_state(States.call)

@router.callback_query(Text(text=['cancel']), StateFilter(States.call))
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    msg = await callback.message.answer("Ok, you will be return to main menu")
    await delete(msg, time=3)
    await callback.message.edit_text("Main Menu",
                                     reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)
    await state.clear()

@router.message(StateFilter(States.call))
async def state_call(message: types.Message, callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(call=message.text)
    user_answer = await state.get_data()
    admin = random.choice(config.tg_bot.admin_ids)
    await bot.send_message(chat_id=admin, text=user_answer['call'])
    msg = await message.reply("Great! We have notified support about your request.")
    await delete(msg, time=3)
    
    await message.answer("Main Menu",
                         reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)
    await state.clear()