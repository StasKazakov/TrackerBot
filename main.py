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
from config import Config, load_config
from redirection.url_flask import UTMTracker
from services import broadcaster
from tools.keyboard import start_menu, menu_getter, cancel_button
from handlers import user_handlers, admin_handlers
from tools.db import Database
from handlers.language_data import Text as Tx

app = Quart(__name__)
config: Config = load_config()
db = Database(config.db.host, config.db.user, config.db.password, config.db.database)
dp: Dispatcher = Dispatcher()
language_data = Tx()


async def on_startup(bot: Bot, admin_ids: int):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


@dp.message(Command('start'))
async def starting(message: types.Message):
    db.add_user(message.from_user.id, str(message.from_user.full_name))
    await message.answer(language_data.choose_language(Tx), reply_markup=start_menu)

@dp.callback_query(Text(text=['en', 'ua', 'ru']))
async def language(callback: types.CallbackQuery, state: FSMContext):
    db.save_language(callback.data, int(callback.from_user.id))
    await callback.answer(callback.message.text, show_alert=False)
    await callback.message.edit_text(text=language_data.menu(db.check_language(int(callback.from_user.id))),
                                     reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)


async def main():
    #logging
    logging.basicConfig(filename="all_log.log", level=logging.INFO, format="%(asctime)s - $(levelname)s - %(message)s")
    bl.basic_colorized_config(level=logging.INFO)

    #connecting all packages and environment variables
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    #adding routers
    dp.include_router(user_handlers.router)

    #starting the bot
    await on_startup(bot, config.tg_bot.admin_ids)
    await handle_request()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
  