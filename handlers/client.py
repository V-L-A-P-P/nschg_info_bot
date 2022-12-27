from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards.client_kb import kb_client


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.message):
    await bot.send_message(message.from_user.id, 'Привет я бот', reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
