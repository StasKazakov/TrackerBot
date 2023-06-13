import logging
import asyncio
import betterlogging as bl
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from quart import Quart
from aiogram.fsm.context import FSMContext
from services import broadcaster
from tools.keyboard import start_menu, menu_getter
from handlers import user_handlers, admin_handlers
from tools.db import Database
from tools.language_data import Text as Tx
from tools.delete import delete
from config import Config, load_config



logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
dp: Dispatcher = Dispatcher()
config: Config = load_config()
db = Database()
language_data = Tx()


async def on_startup(bot: Bot, admin_ids: int):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


@dp.message(Command('start'))
async def starting(message: types.Message):
    await db.add_user(str(message.from_user.id), str(message.from_user.full_name))
    msg = await message.reply(text="Hi👋 This bot will help you keep track amount of clicks on your links!\nLet's get started!")
    await message.answer(language_data.choose_language(Tx), reply_markup=start_menu)
    await delete(msg, 300)

@dp.callback_query(Text(text=['en', 'ua', 'ru']))
async def language(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await db.save_language(str(callback.from_user.id), callback.data)
    lang = await db.check_language(str(callback.from_user.id))
    if await db.add_user(str(callback.from_user.id), str(callback.from_user.full_name)) == False:
        msg = await bot.send_message(callback.from_user.id, text=language_data.message_for_new_user(lang))
        await callback.message.edit_text(text=language_data.menu(lang),
                                     reply_markup=menu_getter(lang), show_alert=False)
        await delete(msg, 300)
    else:
        msg = await bot.send_message(callback.from_user.id, text=language_data.message_for_old_user(lang))
        await callback.message.edit_text(text=language_data.menu(lang),
                                     reply_markup=menu_getter(lang), show_alert=False)


async def main():
    #logging
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    #connecting all packages and environment variables
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    #adding routers
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.admin_router)
    #starting the bot
    await on_startup(bot, config.tg_bot.admin_ids)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
  