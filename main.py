import logging
import asyncio
import betterlogging as bl
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from quart import Quart, redirect
from aiogram.fsm.context import FSMContext
from config import Config, load_config
from services import broadcaster
from tools.keyboard import start_menu, menu_getter, cancel_button
from handlers import user_handlers, admin_handlers
from tools.db import Database
from handlers.language_data import Text as Tx

app = Quart(__name__)
db = Database("TrackerBot.db")
dp: Dispatcher = Dispatcher()
language_data = Tx()


async def on_startup(bot: Bot, admin_ids: int):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


@dp.message(Command('start'))               #start function
async def starting(message: types.Message):
    db.add_user(message.from_user.id, str(message.from_user.full_name))
    lang = db.check_language(message.from_user.id)
    await message.reply("Hi👋 This bot will help you keep track amount of clicks on your links! Let's get started!")
    if lang is not None:
        await message.answer(language_data.for_old_user(lang), reply_markup=menu_getter(lang))
    else:
        await message.answer(language_data.choose_language(Tx), reply_markup=start_menu)

@dp.callback_query(Text(text=['en', 'ua', 'ru']))     #choosing language for new user
async def language(callback: types.CallbackQuery, state: FSMContext):
    db.save_language(callback.data, int(callback.from_user.id))
    await callback.answer(language_data.for_new_user(db.check_language(callback.from_user.id)), show_alert=False, cache_time=5)
    await callback.message.edit_text(text=language_data.menu(db.check_language(int(callback.from_user.id))),
                                     reply_markup=menu_getter(db.check_language(int(callback.from_user.id))), show_alert=False)


async def main():
    #logging
    logging.basicConfig(filename="all_log.log", level=logging.INFO, format="%(asctime)s - $(levelname)s - %(message)s")
    bl.basic_colorized_config(level=logging.INFO)

    #connecting all packages and environment variables
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    #adding routers
    dp.include_router(user_handlers.router)

    #starting the bot
    await on_startup(bot, config.tg_bot.admin_ids)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
  