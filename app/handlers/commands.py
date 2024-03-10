from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

cmd_router = Router()


@cmd_router.message(Command("about"))
async def about_cmd(message: Message):
    await message.answer("Я бот проекта Simple Physics!")
    
@cmd_router.message(Command("contacts"))
async def contacts_cmd(message: Message):
    await message.answer("По всем вопросам обращайтесь к моему создателю: @bratisman")
    
    
@cmd_router.message(Command("faq"))
async def faq_cmd(message: Message):
    await message.answer("В разработке...")
    
    
@cmd_router.message(Command("materials"))
async def materials_cmd(message: Message):
    await message.answer("Подгружаю материалы...")
    await asyncio.sleep(1.5)
    await message.answer("Готово! Вот ссылки на материалы:")