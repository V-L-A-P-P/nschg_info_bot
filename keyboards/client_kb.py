from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import school_documents.documents
from bot_logic_files import bot_files
import school_questions
from school_documents import documents

def get_num_keyboard(count):
    if count <= 7:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    else:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    kb.row(KeyboardButton('⬅Вернуться в меню'))
    kb.row(KeyboardButton(convert_nums_to_buttons("1")))
    for i in range(2, count + 1):
        kb.insert(KeyboardButton(convert_nums_to_buttons(str(i))))
    return kb


def get_kb_docs():
    kb_docs = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_docs.add(KeyboardButton('⬅Вернуться в меню'))
    for key in school_documents.documents.load_doc_dict():
        kb_docs.add(KeyboardButton(key))
    return kb_docs


def get_kb_return_to_menu():
    kb_return_to_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_return_to_menu.add(KeyboardButton("⬅Вернуться в меню"))
    return kb_return_to_menu


def get_kb_client_menu():
    kb_client_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    for b in bot_files.load_main_menu_buttons():
        kb_client_menu.add(KeyboardButton(b))
    return kb_client_menu


def get_kb_client_questions_categories():
    kb_client_questions = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client_questions.add(KeyboardButton('⬅Вернуться в меню'))
    for key in school_questions.school_questions.load_questions():
        kb_client_questions.add(KeyboardButton(key))
    return kb_client_questions


def convert_buttons_to_nums(s):
    s = s.replace("0️⃣", "0")
    s = s.replace("1️⃣", "1")
    s = s.replace("2️⃣", "2")
    s = s.replace("3️⃣", "3")
    s = s.replace("4️⃣", "4")
    s = s.replace("5️⃣", "5")
    s = s.replace("6️⃣", "6")
    s = s.replace("7️⃣", "7")
    s = s.replace("8️⃣", "8")
    s = s.replace("9️⃣", "9")
    return s


def convert_nums_to_buttons(s):
    s = s.replace("0", "0️⃣")
    s = s.replace("1", "1️⃣")
    s = s.replace("2", "2️⃣")
    s = s.replace("3", "3️⃣")
    s = s.replace("4", "4️⃣")
    s = s.replace("5", "5️⃣")
    s = s.replace("6", "6️⃣")
    s = s.replace("7", "7️⃣")
    s = s.replace("8", "8️⃣")
    s = s.replace("9", "9️⃣")
    return s
