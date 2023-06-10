import logging
import asyncio
import betterlogging as bl
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from quart import Quart
from aiogram.fsm.context import FSMContext
from config import Config, load_config
from services import broadcaster
from tools.keyboard import start_menu, menu_getter
from handlers import user_handlers
from tools.db import Database
from TrackerBot.tools.language_data import Text as Tx

app = Quart(__name__)
db = Database("TrackerBot.db")
dp: Dispatcher = Dispatcher()
language_data = Tx()


async def on_startup(bot: Bot, admin_ids: int):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


@dp.message(Command('start'))
async def starting(message: types.Message):
    await db.add_user(str(message.from_user.id), str(message.from_user.full_name))
    await message.reply(text="Hi👋 This bot will help you keep track amount of clicks on your links!\nLet's get started!")
    await message.answer(language_data.choose_language(Tx), reply_markup=start_menu)

@dp.callback_query(Text(text=['en', 'ua', 'ru']))
async def language(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await db.save_language(callback.data, str(callback.from_user.id))
    lang = await db.check_language(str(callback.from_user.id))
    await bot.send_message(callback.from_user.id, text=language_data.message_for_new_user(lang))
    await callback.message.edit_text(text=language_data.menu(lang),
                                     reply_markup=menu_getter(lang), show_alert=False)


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
  