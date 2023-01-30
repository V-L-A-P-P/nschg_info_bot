from aiogram.utils import executor
from create_bot import dp
from handlers import client_handlers, admin_handlers


async def on_startup(_):
    print("bot is online now")

client_handlers.register_handlers_client(dp)
admin_handlers.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
