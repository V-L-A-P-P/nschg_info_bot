from aiogram import types, Dispatcher
import school_documents.documents
from keyboards import admin_kb, client_kb
from school_questions import school_questions
from create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from school_operator import operator


class FSMAdmin(StatesGroup):
    getting_category = State()
    getting_new_question = State()
    getting_new_answer = State()

    getting_new_doc_name = State()
    getting_new_doc = State()


async def command_start(message: types.message):
    print('ha')
    if message.from_user.id == operator.get_operator_id():
        print(message.from_user.id)
        await bot.send_message(operator.get_operator_id(), message)
        await bot.send_message(message.from_user.id, 'Привет я бот', reply_markup=admin_kb.get_kb_admin_menu())


async def open_menu_command(message: types.message, state: FSMContext):
    if message.from_user.id == operator.get_operator_id():
        print('haha')
        await state.finish()
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=admin_kb.get_kb_admin_menu())
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=client_kb.get_kb_client_menu())


async def new_question_start(message: types.Message):
    if message.from_user.id == operator.get_operator_id():
        await FSMAdmin.getting_category.set()

        await message.reply(f"Введите новую категорию вопроса или уже существующую:",
                            reply_markup=client_kb.get_kb_client_questions_categories())
    else:
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=client_kb.get_kb_client_menu())




async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMAdmin.getting_new_question.set()
    await message.reply("Введите новый вопрос:")


async def load_new_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_question'] = message.text
    await FSMAdmin.getting_new_answer.set()
    await message.reply("Введите ответ на вопрос:")


async def load_new_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_answer'] = message.text
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id,
                               "Новый вопрос добавлен",
                               reply_markup=admin_kb.get_kb_admin_menu())
        school_questions.add_new_question(data['new_question'], data['new_answer'], data['category'])
    await state.finish()



async def new_doc_start(message: types.Message):
    if message.from_user.id == operator.get_operator_id():
        await FSMAdmin.getting_new_doc_name.set()
        await message.reply(f"Введите имя для нового документа:", reply_markup=admin_kb.get_kb_return_to_menu())
    else:
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=client_kb.get_kb_client_menu())

async def load_new_doc_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_doc_name'] = message.text
    await FSMAdmin.getting_new_doc.set()
    await message.reply(f"Пришлите новый документ:", reply_markup=admin_kb.get_kb_return_to_menu())

async def load_new_doc(message: types.Document, state: FSMContext):
    print('blin')
    extension = message['document']['file_name'].split('.')[len(message['document']['file_name'].split('.')) - 1]
    async with state.proxy() as data:
        await school_documents.documents.dump_doc_from_message(message, data['new_doc_name'], extension)
        school_documents.documents.add_new_doc_name(data['new_doc_name'], extension)
    await bot.send_message(message.from_user.id, "Новый документ добавлен")
    await state.finish()
