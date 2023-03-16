from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_logic_files import bot_files


def get_kb_admin_menu():
    kb_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    for b in bot_files.load_admin_menu_buttons():
        kb_admin_menu.add(KeyboardButton(b))
    return kb_admin_menu

def get_kb_return_to_menu():
    kb_return_to_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_return_to_menu.add(KeyboardButton("⬅Вернуться в меню"))
    return kb_return_to_menu