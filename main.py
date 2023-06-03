import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from keyboard import start_menu, main_menu
from db import Database

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN_past'))
dp = Dispatcher()
db = Database("TrackerBot.db")


@dp.message(Command('start'))
async def starting(message: types.Message, bot: Bot):
    db.add_user(message.from_user.id)
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
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
