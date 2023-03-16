import json
from create_bot import bot
from aiogram import types

def load_doc_dict():
    try:
        with open('school_documents/doc_names.json', 'r', encoding='utf8') as f:
            doc_dict = json.load(f)
        print(doc_dict)
        return doc_dict
    except FileNotFoundError:
        print("Error: файл с документами отсутствует")


async def dump_doc_from_message(message: types.Document, name, extension):
    k = await bot.get_file(message.document.file_id)
    await bot.download_file(k.file_path, f"school_documents/{name}.{extension}")

def add_new_doc_name(name, extension):
    try:
        doc_names = load_doc_dict()
        doc_names[name] = f"{name}.{extension}"
        with open(f'school_documents/doc_names.json', 'w', encoding='utf8') as f:
            json.dump(doc_names, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Error: файл с документами отсутствует")
