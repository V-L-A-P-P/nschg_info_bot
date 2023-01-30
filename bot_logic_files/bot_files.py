import json
import os


def load_main_menu_buttons():
    try:
        with open('bot_logic_files/main_menu_buttons.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Файл с кнопками меню отсутствует")