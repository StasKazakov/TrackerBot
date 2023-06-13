from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message
from tools.db import Database
from config import Config, load_config
from filters.admin import AdminFilter

config: Config = load_config()
db = Database()
admin_router = Router()
admin_router.message(AdminFilter(), config)


@admin_router.message(Command("hi"))
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")