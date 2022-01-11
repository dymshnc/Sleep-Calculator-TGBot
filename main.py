import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)

if __name__ == "__main__":
    from admin.admin_handlers import dp, send_to_admin
    from users.users_handlers import dp

    executor.start_polling(dp, on_startup=send_to_admin)
