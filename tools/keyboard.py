from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='English', callback_data="en")],
    [types.InlineKeyboardButton(text='Українська', callback_data='ua')],
    [types.InlineKeyboardButton(text='Русский', callback_data="ru")]
], )

main_menu_text_eng = {'Add link': 'link', 'Statistics': 'state', 'Instruction': 'help', 'Contact us': 'call'}
main_menu_text_ua = {'Додати посилання': 'link', 'Статистика': 'state', 'Допомога': 'help', "Зворотній зв'язок": 'call'}
main_menu_text_ru = {'Добавление ссылки': 'link', 'Статистика': 'state', 'Помощь': 'help', 'Обратная связь': 'call'}

def article_getter(lang, article) -> InlineKeyboardMarkup:
    return None

def menu_getter(lang) -> InlineKeyboardMarkup:
    if lang == 'en':
        main_menu = InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=text, callback_data=data)] for text, data in
                             main_menu_text_eng.items()])
        return main_menu

    elif lang == 'ua':
        main_menu = InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=text, callback_data=data)] for text, data in
                             main_menu_text_ua.items()])
        return main_menu

    elif lang == 'ru':
        main_menu = InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=text, callback_data=data)] for text, data in
                             main_menu_text_ru.items()])
        return main_menu

def cancel_button(lang) -> InlineKeyboardMarkup:
    if lang == 'en':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Cancel', callback_data='cancel')]])
        return button
    elif lang == 'ua':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Відміна дії', callback_data='cancel')]])
        return button
    elif lang == 'ru':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Отмена', callback_data='cancel')]])
        return button
