from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.filters.chat_type import ChatTypeFilter


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')