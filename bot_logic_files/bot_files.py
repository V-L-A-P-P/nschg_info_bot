import json


def dump_new_logic_file(file, name):
    with open(f'bot_logic_files/{name}.json', 'w', encoding='utf8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)


def load_admin_menu_buttons():
    try:
        with open('bot_logic_files/admin_menu_buttons.json', 'r', encoding='utf8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Файл с кнопками меню админа отсутствует")


def load_main_menu_buttons():
    try:
        with open('bot_logic_files/main_menu_buttons.json', 'r', encoding='utf8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Файл с кнопками меню отсутствует")

# a = ["Добавить новый вопрос", "Добавить новый документ"]
# dump_new_logic_file(a, "admin_menu")