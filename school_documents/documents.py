import json
from create_bot import bot
from aiogram import types

def load_doc():
    try:
        with open('school_documents/doc_names.json', 'r', encoding='utf8') as f:
            doc_dict = json.load(f)
        print(doc_dict)
        return doc_dict
    except FileNotFoundError:
        print("Error: файл с документами отсутствует")

async def dump_doc_from_message(message: types.Document, name):
    k = await bot.get_file(message.document.file_id)
    await bot.download_file(k.file_path, "school_questions/text1.pdf")
