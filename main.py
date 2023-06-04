import logging
import asyncio
import os
from urllib.parse import urlparse, parse_qs

import betterlogging as bl
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from quart import Quart, redirect
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import load_config
from redirection.url_flask import UTMTracker
from services import broadcaster
from tools.keyboard import start_menu, main_menu, cancel_button
from tools.db import Database

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
app = Quart(__name__)
load_dotenv()

bot = Bot(token="5989058480:AAGOgpWR7AKu145jA9urg1EqBDUw-TAy3V4") # bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
db = Database("TrackerBot.db")
help_id = "2067639356" # ID of the person who will receive requests
# help_id = os.getenv('ADMIN_ID')

class States(StatesGroup):
    call = State()
    
async def delete(msg):
    try:
        await msg.delete()
    
    except Exception as e:
        pass


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")
    

@dp.message(Command('start'))
async def starting(message: types.Message):
    db.add_user(message.from_user.id, str(message.from_user.last_name))
    await message.answer('Hello!\n Please, choose your language:', reply_markup=start_menu)


@dp.callback_query(Text(text=['en', 'ua', 'ru']))
async def language(callback: types.CallbackQuery):
    await callback.answer(callback.message.text, show_alert=False)
    await callback.message.edit_text(text='Choose the option', reply_markup=main_menu, show_alert=False)


@dp.callback_query(Text(text=['link']))
async def answer_menu(callback:types.CallbackQuery):
    if callback.message.text != 'Add link':
        await callback.message.edit_text(text='Add link', reply_markup=main_menu, show_alert=False)
    await callback.answer()


@dp.callback_query(Text(text=['state']))
async def answer_menu(callback:types.CallbackQuery):
    if callback.message.text != 'Statistics':
        await callback.message.edit_text(text='Statistics', reply_markup=main_menu, show_alert=False)
    await callback.answer()


@dp.callback_query(Text(text=['help']))
async def answer_menu(callback:types.CallbackQuery):
    if callback.message.text != 'Instruction':
        await callback.message.edit_text(text='Instruction', reply_markup=main_menu, show_alert=False)
    await callback.answer()


@dp.callback_query(Text(text=['call']))
async def answer_menu(callback:types.CallbackQuery, state: FSMContext ):
    await callback.message.edit_text(text='Ok, send your request below', reply_markup= cancel_button)
    await state.set_state(States.call)
    
    
@dp.callback_query(Text(text=['cancl']))
async def cancel(callback:types.CallbackQuery):
    msg = await callback.message.answer("Ok, you will be return to main menu")
    await asyncio.sleep(2)
    await delete(msg)
    await callback.message.edit_text("Main Menu", reply_markup = main_menu, show_alert = False)
    

@dp.message(States.call)
async def state_call(message: types.Message, state: FSMContext, bot: Bot ):
    await state.update_data(call = message.text)
    user_answer = await state.get_data()
    await bot.send_message(help_id, user_answer['call'])
    msg = await message.answer("Great! We have notified support about your request.")
    await message.answer("Main Menu", reply_markup = main_menu, show_alert = False)
    await asyncio.sleep(5)
    await delete(msg)
    await state.clear()


@app.route('/', methods=['GET'])
async def handle_request():
    g = ['utm_source', 'utm_medium', 'utm_campaign', 'datetime']
    redirect_url = UTMTracker('https://t.me/botfatherdev', 'Telegram', 'adv', 'new service').add_utm_params()
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    params_list = [f"{i}: {query_params.get(i, [''])[0]}" for i in g]
    logging.info(params_list)
    return redirect(parsed_url.geturl())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config(".env")
    await on_startup(bot, config.tg_bot.admin_ids)
    await handle_request()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    app.run(host='0.0.0.0', port=8000)


