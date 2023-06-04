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

from config import load_config
from redirection.url_flask import UTMTracker
from services import broadcaster
from tools.keyboard import start_menu, main_menu
from tools.db import Database

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
app = Quart(__name__)
load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
db = Database("TrackerBot.db")


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
async def answer_menu(callback:types.CallbackQuery):
    if callback.message.text != 'Contact us':
        await callback.message.edit_text(text='Contact us', reply_markup=main_menu, show_alert=False)
    await callback.answer()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config(".env")
    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    @app.route('/', methods=['GET'])
    async def handle_request():
        g = ['utm_source', 'utm_medium', 'utm_campaign', 'datetime']
        redirect_url = UTMTracker('https://t.me/botfatherdev', 'Telegram', 'adv', 'new service').add_utm_params()
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        params_list = [f"{i}: {query_params.get(i, [''])[0]}" for i in g]
        print(*params_list, sep='\n')
        return redirect(parsed_url.geturl())


    if __name__ == '__main__':
        asyncio.run(main())
        app.run(host='0.0.0.0', port=8000)

