import asyncio, os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

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
    await message.answer(f'Я бот проекта <b>SIMPLE PHYSICS!</b>', parse_mode='HTML')
    await asyncio.sleep(0.5)
    
    # Check if user is admin
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("⬇️Выберите дальнейшее действие⬇️", 
                             reply_markup=rp.start_admin)
        await message.answer("Вы вошли как администратор!")
    else:
        await message.answer("⬇️Выберите дальнейшее действие⬇️", 
                             reply_markup=rp.start)
        
        
# INFO ABOUT BOT
@common_router.message(F.text == "🤖Информация о боте")
async def about_bot(message: Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAPUZdtMgrKCGWN1hGG7sC9lB1Ob2nIAAhsTAAJakthIYwemdV7Qq5c0BA", 
                                 reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer("Моя основная задача - предоставлять вам учебные материалы по физике!")
    await asyncio.sleep(0.7)
    await message.answer("По сути, я являюсь хранилищем всего самого полезного, что создается командой Simple Physics")
    await asyncio.sleep(0.7)
    
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Переходите на наш канал, где еженедельно выпускается много интересного и познавательного контента:\n\n https://t.me/simplephysics_polyteh',
                             reply_markup=rp.start_admin)
    else:
        await message.answer(f'Переходите на наш канал, где еженедельно выпускается много интересного и познавательного контента:\n\n https://t.me/simplephysics_polyteh',
                             reply_markup=rp.start)
    
    
# ECHO HANDLER
@common_router.message()
async def echo(message: Message):
    await message.answer("Я не понимаю")