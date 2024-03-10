import asyncio, os

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.dao import get_docs_by_material, get_material_by_name, get_doc_by_name
from app.keyboards import reply as rp
from app.keyboards import builder


from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

materials_router = Router()


class Materials(StatesGroup):
    material = State()
    document = State()


# ------------ GET MATERIALS start ----------

@materials_router.message(F.text == 'Материалы')
async def get_materials_start(message: Message, state: FSMContext):
    await state.set_state(Materials.material)
    await message.answer("Подгружаю материалы...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.7)
    await message.answer("Готово! Вот ссылки на материалы:", 
                         reply_markup=builder.get_materials_kb())
    
    
@materials_router.callback_query(Materials.material)
async def choose_material(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Вернуться к меню':
        await state.clear()
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start_admin)
        else:
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start)
        await callback.message.delete()
    else:
        await state.update_data(material=callback.data)
        await state.set_state(Materials.document)
        material = await get_material_by_name(callback.data)
        material_id = material[0]
        await callback.message.edit_text("Выберите документ:", 
                                        reply_markup=builder.get_docs_kb(material_id))
    
    
@materials_router.callback_query(Materials.document)
async def get_material_document(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Вернуться':
        await state.set_state(Materials.material)
        await callback.message.edit_text("Материалы:", reply_markup=builder.get_materials_kb())
    else:
        await state.update_data(document=callback.data)
        await callback.message.delete()
        data = await state.get_data()
        
        doc = await get_doc_by_name(data.get("document"))
        
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            await callback.message.answer_document(doc[3], reply_markup=rp.start_admin)
        else:
            await callback.message.answer_document(doc[3], reply_markup=rp.start)
        
        state.clear()
        
# ------------ GET MATERIALS end ----------