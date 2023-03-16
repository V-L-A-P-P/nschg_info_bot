from aiogram.utils import executor
from create_bot import dp
from handlers import handlers_registration


async def on_startup(_):
    print("bot is online now")

handlers_registration.register_handlers_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
