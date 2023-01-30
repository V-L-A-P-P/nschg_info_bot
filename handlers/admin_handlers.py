from aiogram import types, Dispatcher
import school_documents.documents
from school_questions import school_questions
from create_bot import bot
import keyboards.client_kb as client_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from school_operator import operator
from aiogram.types import InputFile


class FSMAdmin(StatesGroup):
    getting_category = State()
    getting_new_question = State()
    getting_new_answer = State()

    getting_new_file = State()
    getting_new_file_name = State()


async def new_question_start(message: types.Message):
    await FSMAdmin.getting_category.set()

    await message.reply(f"Введите новую категорию вопроса или уже существующую({str(school_questions.load_questions().keys())}):",
                        reply_markup=client_kb.get_kb_return_to_menu())



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
                               reply_markup=client_kb.get_kb_client_menu())
        school_questions.add_new_question(data['new_question'], data['new_answer'], data['category'])
    await state.finish()



async def new_doc_start(message: types.Message):
    await FSMAdmin.getting_new_file.set()

    await message.reply(f"Добавьте новый файл:", reply_markup=client_kb.get_kb_return_to_menu())



async def load_new_file(message: types.Document, state: FSMContext):
    print('ha')
    async with state.proxy() as data:
        pass
    await FSMAdmin.getting_new_question.set()


    await school_documents.documents.dump_file_from_message(message)


async def load_new_file_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_answer'] = message.text
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id,
                               "Новый вопрос добавлен",
                               reply_markup=client_kb.get_kb_client_menu())
        school_questions.add_new_question(data['new_question'], data['new_answer'], data['category'])
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(new_question_start, text='addques')
    dp.register_message_handler(load_category, state=FSMAdmin.getting_category)
    dp.register_message_handler(load_new_question, state=FSMAdmin.getting_new_question)
    dp.register_message_handler(load_new_answer, state=FSMAdmin.getting_new_answer)

    dp.register_message_handler(new_doc_start, text='A')
    dp.register_message_handler(load_new_file, state=FSMAdmin.getting_new_file, content_types=["document"])
    dp.register_message_handler(load_new_answer, state=FSMAdmin.getting_new_answer)