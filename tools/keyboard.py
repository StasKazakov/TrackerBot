from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='English', callback_data="en")],
    [types.InlineKeyboardButton(text='Українська', callback_data='ua')],
    [types.InlineKeyboardButton(text='Русский', callback_data="ru")]
], )

main_menu_text_eng = {'Add link': 'link', 'Statistics': 'state', 'Instruction': 'help', 'Contact us': 'call'}
main_menu_text_ua = {'Додати посилання': 'link', 'Статистика': 'state', "Інструкція": 'help', "Контакти": 'call'}
main_menu_text_ru = {'Добавление ссылки': 'link', 'Статистика': 'state', "Инструкция": 'help', "Контакты": 'call'}

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

def cancel_button(lang: str) -> InlineKeyboardMarkup:
    if lang == 'en':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Cancel', callback_data='cancel')]])
        return button
    elif lang == 'ua':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Відміна дії', callback_data='cancel')]])
        return button
    elif lang == 'ru':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Отмена', callback_data='cancel')]])
        return button

def back_button(lang: str) -> InlineKeyboardMarkup:
    if lang == 'en':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Back', callback_data='back')]])
        return button
    elif lang == 'ua':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Назад', callback_data='back')]])
        return button
    elif lang == 'ru':
        button = InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Назад', callback_data='back')]])
        return button

def periods(lang: str) -> InlineKeyboardMarkup:
    if lang == 'en':
        button = InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="All time", callback_data='alltime')],
            [types.InlineKeyboardButton(text='Select dates', callback_data='select_dates')]])
        return button
    elif lang == 'ua':
        button = InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="За весь період", callback_data='alltime')],
            [types.InlineKeyboardButton(text="Вибрати дати", callback_data='select_dates')]])
        return button
    elif lang == 'en':
        button = InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="За весь период", callback_data='alltime')],
            [types.InlineKeyboardButton(text="Выбрать даты", callback_data='select_dates')]])
        return button
    
def links(links_name: list) -> InlineKeyboardMarkup:
    pass
    # callback_data = []
    # for i in range(len(links_name)):
    #    callback_data.append(f"callback_{i}")
    # links_dict = dict(zip(links_name, callback_data))
    # inline_keyboards = []
    # for text, data in links_dict.items():
    #    inline_keyboards.append([types.InlineKeyboardButton(text=text, callback_data=data)])
    # links = InlineKeyboardMarkup(inline_keyboard= inline_keyboards)
    # return links