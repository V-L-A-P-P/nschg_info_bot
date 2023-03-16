from aiogram import types

import school_documents.documents
from handlers import admin_handlers
from school_questions import school_questions
from create_bot import bot
import keyboards.client_kb as client_kb
import keyboards.admin_kb as admin_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from school_operator import operator
from aiogram.types import InputFile


# bot's state class when it receives an appeal to the administration
class FSMClient(StatesGroup):
    name = State()
    surname = State()
    contact = State()
    appeal = State()

    choose_categories = State()
    giving_answer = State()

    choose_doc = State()


async def command_start(message: types.message):
    if message.from_user.id != operator.get_operator_id():
        print(message.from_user.id)
        await bot.send_message(operator.get_operator_id(), message)
        await bot.send_message(message.from_user.id, 'Привет, я бот школы НЧШ\nИспользуй меню:', reply_markup=client_kb.get_kb_client_menu())
    else:
        await admin_handlers.command_start(message)


async def open_menu_command(message: types.message, state: FSMContext):
    if message.from_user.id != operator.get_operator_id():
        await state.finish()
        await bot.send_message(message.from_user.id, 'Меню', reply_markup=client_kb.get_kb_client_menu())
    else:
        await admin_handlers.open_menu_command(message, state)



async def new_operator_command(message: types.message, state: FSMContext):
    operator.change_operator(message.from_user.id)

    await bot.send_message(message.from_user.id,
                           'Вы успешно зарегистрированы как новый оператор',
                            reply_markup=admin_kb.get_kb_admin_menu())
    await state.finish()


async def school_questions_command(message: types.message):
    if message.from_user.id != operator.get_operator_id():
        await FSMClient.choose_categories.set()
        await bot.send_message(message.from_user.id, 'Выберите категорию:',
                               reply_markup=client_kb.get_kb_client_questions_categories())


async def choosing_questions_categories_command(message: types.message, state: FSMContext):
    if message.text in school_questions.load_questions().keys():
        async with state.proxy() as data:
            data['category'] = message.text
        print('hello')
        await FSMClient.giving_answer.set()
        await bot.send_message(message.from_user.id,
                               school_questions.get_str_questions(message.text),
                               reply_markup=client_kb.get_num_keyboard(
                                   len(school_questions.load_questions()[message.text])))


async def choosing_question_command(message: types.message, state: FSMContext):
    if not message.text.isdigit() and not client_kb.convert_buttons_to_nums(message.text).isdigit():
        return None
    if message.text.isdigit():
        async with state.proxy() as data:
            await bot.send_message(message.from_user.id,
                                   school_questions.find_answer_by_num(int(message.text), data['category']))
    else:
        async with state.proxy() as data:
            await bot.send_message(message.from_user.id,
                                   school_questions.find_answer_by_num(
                                       int(client_kb.convert_buttons_to_nums(message.text)),
                                       data['category']
                                       ))


async def show_docs_buttons_command(message: types.message):
    if message.from_user.id != operator.get_operator_id():
        await FSMClient.choose_doc.set()
        await bot.send_message(message.from_user.id, 'Выберите документ:', reply_markup=client_kb.get_kb_docs())


async def choose_doc_command(message: types.message, state: FSMContext):
    if message.text in list(school_documents.documents.load_doc_dict().keys()):
        await bot.send_message(message.from_user.id, "Пожалуйста подождите, файл загружается...",
                               reply_markup=client_kb.get_kb_client_menu())
        file_name = school_documents.documents.load_doc_dict()[message.text]
        extension = file_name.split('.')[len(file_name.split('.')) - 1]
        await bot.send_document(message.from_user.id,
                            InputFile(f"school_documents/{file_name}",
                            filename=f"{message.text}.{extension}"))
        await state.finish()


# APPEAL TO THE ADMINISTRATION
async def cm_start(message: types.Message):
    if message.from_user.id != operator.get_operator_id():
        await FSMClient.name.set()

        await message.reply("Введите имя и фамилию:", reply_markup=client_kb.get_kb_return_to_menu())


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.contact.set()
    await message.reply("Введите ваш контакт( Номер телефона или почта для связи ):")


async def load_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
    await FSMClient.next()
    await message.reply("Введите ваше обращение:")


async def load_appeal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['appeal'] = message.text
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id,
                               "Ваще обращение успешно принято и будет обработано в ближайшее время",
                               reply_markup=client_kb.get_kb_client_menu())
        await bot.send_message(operator.get_operator_id(),
                               f"*Новое обращение*\n\nКонтактные данные:\n{data['name']}, {data['contact']}\n\nТекст обращения:\n{data['appeal']}")
    await state.finish()

