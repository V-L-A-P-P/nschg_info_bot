import handlers.admin_handlers as admin_handlers
import handlers.client_handlers as client_handlers
from aiogram import Dispatcher
import school_documents.documents
from school_questions import school_questions

def register_handlers_admin(dp: Dispatcher):
    # common handlers
    dp.register_message_handler(client_handlers.open_menu_command, text=['⬅Вернуться в меню'], state="*")
    dp.register_message_handler(client_handlers.command_start, commands=['start', 'help'])

    # admin handlers
    dp.register_message_handler(admin_handlers.new_question_start, text='Добавить новый вопрос')
    dp.register_message_handler(admin_handlers.load_category, state=admin_handlers.FSMAdmin.getting_category)
    dp.register_message_handler(admin_handlers.load_new_question, state=admin_handlers.FSMAdmin.getting_new_question)
    dp.register_message_handler(admin_handlers.load_new_answer, state=admin_handlers.FSMAdmin.getting_new_answer)

    dp.register_message_handler(admin_handlers.new_doc_start, text='Добавить новый документ')
    dp.register_message_handler(admin_handlers.load_new_doc_name, state=admin_handlers.FSMAdmin.getting_new_doc_name)
    dp.register_message_handler(admin_handlers.load_new_doc,
                                state=admin_handlers.FSMAdmin.getting_new_doc,
                                content_types="document")

    # client handlers
    dp.register_message_handler(client_handlers.new_operator_command, text='admin', state="*")

    dp.register_message_handler(client_handlers.school_questions_command, text=['Вопросы и ответы'])
    dp.register_message_handler(client_handlers.choosing_questions_categories_command,
                                state=client_handlers.FSMClient.choose_categories)
    dp.register_message_handler(client_handlers.choosing_question_command,
                                state=client_handlers.FSMClient.giving_answer)

    dp.register_message_handler(client_handlers.show_docs_buttons_command, text=['Документы'])
    dp.register_message_handler(client_handlers.choose_doc_command,
                                state=client_handlers.FSMClient.choose_doc)


    dp.register_message_handler(client_handlers.cm_start, text=['Написать администрации'])
    dp.register_message_handler(client_handlers.load_name, state=client_handlers.FSMClient.name)
    dp.register_message_handler(client_handlers.load_contact, state=client_handlers.FSMClient.contact)
    dp.register_message_handler(client_handlers.load_appeal, state=client_handlers.FSMClient.appeal)
    dp.register_message_handler(client_handlers.open_menu_command)
