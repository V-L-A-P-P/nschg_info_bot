import json
names = ["Вопросы и ответы", "Документы", "Написать администрации"]

with open('main_menu_buttons.json', 'w', encoding='utf8') as f:
    json.dump(names, f, ensure_ascii=False, indent=4)