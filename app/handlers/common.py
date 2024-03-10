import asyncio, os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.dao import add_user
from app.keyboards import reply as rp


from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


common_router = Router()

# /start command handler
@common_router.message(CommandStart())
async def start_cmd(message: Message):
    # Add user to database
    await add_user(message.from_user.id, message.from_user.username)
    
    # Greet user
    await message.answer_sticker(sticker="CAACAgIAAxkBAAOfZdtFktnm8G3UklmN5pZy7Yv1VpoAAtQMAAJ6i6BIni8iJJQzvJs0BA")
    await asyncio.sleep(1)
    await message.answer(f'Добро пожаловать, {message.from_user.full_name}!')
    await message.answer(f'Я бот проекта Simple Physics!')
    await asyncio.sleep(1)
    
    # Check if user is admin
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Для просмотра материалов нажмите на кнопку ниже:", 
                             reply_markup=rp.start_admin)
        await message.answer("Вы вошли как администратор!")
    else:
        await message.answer("Для просмотра материалов нажмите на кнопку ниже:", 
                             reply_markup=rp.start)
    
    
@common_router.message()
async def echo(message: Message):
    await message.answer("Я не понимаю")