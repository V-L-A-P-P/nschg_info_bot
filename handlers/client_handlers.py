from aiogram import types, Dispatcher

import school_documents.documents
from school_questions import school_questions
from create_bot import bot
import keyboards.client_kb as client_kb
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
    print(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Привет я бот', reply_markup=client_kb.get_kb_client_menu())


async def open_menu_command(message: types.message, state: FSMContext):
    print('huy')
    await state.finish()
    await bot.send_message(message.from_user.id, 'Меню', reply_markup=client_kb.get_kb_client_menu())


async def new_operator_command(message: types.message):
    operator.change_operator(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Вы успешно зарегистрированы как новый оператор')

async def school_questions_command(message: types.message):
    await FSMClient.choose_categories.set()
    await bot.send_message(message.from_user.id, 'Выберите категорию:',
                           reply_markup=client_kb.get_kb_client_questions())


async def choosing_questions_categories_command(message: types.message, state: FSMContext):
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
    await FSMClient.choose_doc.set()
    await bot.send_message(message.from_user.id, 'Выберите документ:', reply_markup=client_kb.get_kb_docs())


async def choose_doc_command(message: types.message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Пожалуйста подождите, файл загружается...")
    await bot.send_document(message.from_user.id,
                        InputFile(f"school_documents/{school_documents.documents.load_doc()[message.text]}",
                        filename=f"{message.text}.pdf"))


# APPEAL TO THE ADMINISTRATION
async def cm_start(message: types.Message):
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
                               f"*Новое обращение*\n\nКонтактные данные:\n{data['name']}, {data['contact']}\nТекст обращения:\n{data['appeal']}")
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(open_menu_command, text=['⬅Вернуться в меню'], state="*")
    dp.register_message_handler(command_start, commands=['start', 'help'])

    dp.register_message_handler(school_questions_command, text=['Вопросы и ответы'])
    dp.register_message_handler(choosing_questions_categories_command,
                                text=school_questions.load_questions().keys(), state=FSMClient.choose_categories)
    dp.register_message_handler(choosing_question_command, state=FSMClient.giving_answer)

    dp.register_message_handler(show_docs_buttons_command, text=['Документы'])
    dp.register_message_handler(choose_doc_command,
                                text=list(school_documents.documents.load_doc().keys()),
                                state=FSMClient.choose_doc)

    dp.register_message_handler(new_operator_command, text='admin')
    dp.register_message_handler(cm_start, text=['Написать администрации'])
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_contact, state=FSMClient.contact)
    dp.register_message_handler(load_appeal, state=FSMClient.appeal)
