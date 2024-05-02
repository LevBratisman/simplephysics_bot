from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio, os
from dotenv import load_dotenv, find_dotenv

from app.keyboards import reply as rp
from app.handlers.materials import get_materials_start
from app.handlers.common import about_bot

cmd_router = Router()

load_dotenv(find_dotenv())


# /about command handler
@cmd_router.message(Command("about"))
async def about_cmd(message: Message, state: FSMContext):
    await state.clear()
    await about_bot(message)
    
    
# /contacts command handler
@cmd_router.message(Command("contacts"))
async def contacts_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'По всем вопросам обращайтесь к моему создателю: @bratisman\n\n' +
                         f'Наш канал: @simplephysics_polyteh')
        
    
# /materials command handler
@cmd_router.message(Command("materials"))
async def materials_cmd(message: Message, state: FSMContext):
    await state.clear()
    await get_materials_start(message, state)
    
    
# /menu command handler
@cmd_router.message(Command("menu"))
async def menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Меню", reply_markup=rp.start_admin)
    else:
        await message.answer("Меню", reply_markup=rp.start)