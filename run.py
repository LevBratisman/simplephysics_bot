import asyncio, os, logging
from dotenv import load_dotenv, find_dotenv

from aiogram import Dispatcher, Bot

from app.database.init import db_start
from app.cmd_list import private
from app.handlers.common import common_router
from app.handlers.commands import cmd_router
from app.handlers.admin.base import admin_router
from app.handlers.admin.materials_settings import materials_settings_router
from app.handlers.admin.documents_settings import documents_settings_router
from app.handlers.materials import materials_router



load_dotenv(find_dotenv())

dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'))


# Database init
async def on_startup():
    await db_start()


async def main():
    
    # Include routers
    dp.include_router(cmd_router)
    dp.include_router(admin_router)
    dp.include_router(materials_settings_router)
    dp.include_router(documents_settings_router)
    dp.include_router(materials_router)
    dp.include_router(common_router)
    
    # Start bot
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(private)
    await dp.start_polling(bot)


# START BOT
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")