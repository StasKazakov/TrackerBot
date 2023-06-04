from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='English', callback_data="en")],
    [types.InlineKeyboardButton(text='Українська', callback_data='ua')],
    [types.InlineKeyboardButton(text='Русский', callback_data="ru")]
], )

main_menu_text = ['Add link', 'Statistics', 'Instruction', 'Contact us']
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Add link', callback_data='link')],
    [types.InlineKeyboardButton(text='Statistics', callback_data='state')],
    [types.InlineKeyboardButton(text='Instruction', callback_data='help')],
    [types.InlineKeyboardButton(text='Contact us', callback_data='call')],
])

cancel_button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Cancel', callback_data='cancl')]])

