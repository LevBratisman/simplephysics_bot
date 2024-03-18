from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.reply import get_keyboard
from app.filters.admin import IsAdmin

admin_private_router = Router()
admin_private_router.message.filter(IsAdmin())
admin_private_router.callback_query.filter(IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    "Выйти из админ панели",
    placehoder="Выберите действие",
    sizes=(2, 1)
)

@admin_private_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("Вы зашли в админ панель", reply_markup=ADMIN_KB)
    
    
@admin_private_router.message(F.text=="Выйти из админ панели")
async def leave_admin_panel(message: Message):
    await message.answer("Вы вышли из админ панели", reply_markup=ReplyKeyboardRemove())