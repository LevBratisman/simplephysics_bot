import asyncio

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.dao import get_materials_all, get_docs_all


# ---------Materials keyboard----------

data = asyncio.run(get_materials_all())

def get_materials_kb():
    kb = InlineKeyboardBuilder()
    for material in data:
        kb.add(InlineKeyboardButton(text=material[1], callback_data=material[1]))
    return kb.adjust(1).as_markup(resize_keyboard=True)

async def update_materials_kb():
    global data
    data = await get_materials_all()
    
    
# ---------Documents keyboard----------

docs_data = asyncio.run(get_docs_all())

def get_docs_kb(catalog_id):
    kb = InlineKeyboardBuilder()
    for doc in docs_data:
        if doc[2] == catalog_id:
            kb.add(InlineKeyboardButton(text=doc[1], callback_data=doc[1]))
    return kb.adjust(2).as_markup(resize_keyboard=True)

async def update_docs_kb():
    global docs_data
    docs_data = await get_docs_all()