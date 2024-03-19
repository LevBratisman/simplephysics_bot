import os, asyncio, logging

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from app.handlers.user_group import user_group_router
from app.handlers.user_private import user_private_router
from app.handlers.admin_private import admin_private_router


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

bot.my_admins_list = []

async def main():
    dp.include_router(user_group_router)
    dp.include_router(user_private_router)
    dp.include_router(admin_private_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")