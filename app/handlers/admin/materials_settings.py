from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.filters import AdminFilter
from app.database.dao import add_material, del_material
from app.keyboards import builder

from app.keyboards import reply as rp
from app.keyboards import inline as inl

materials_settings_router = Router()


class AddMaterial(StatesGroup):
    name = State()
    confirmation = State()
    

class DeleteMaterial(StatesGroup):
    name = State()
    confirmation = State() 


# ---------- ADD MATERIAL start ----------

@materials_settings_router.message(AdminFilter(), F.text == 'Добавить материал')
async def add_material_start(message: Message, state: FSMContext):
    await state.set_state(AddMaterial.name)
    await message.answer("Напишите название материала")
    
@materials_settings_router.message(AddMaterial.name)
async def add_material_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMaterial.confirmation)
    await message.answer("Вы уверены, что хотите добавить этот материал?", 
                         reply_markup=inl.confirm)
    
    
@materials_settings_router.callback_query(AddMaterial.confirmation)
async def add_material_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        name = data.get("name")
        await add_material(name)
        await callback.message.answer(f"Материал '{name}' успешно добавлен!")
        await builder.update_materials_kb()
    else:
        await callback.message.answer("Действие отменено")
    await callback.message.delete()
    await state.clear()
    
# ---------- ADD MATERIAL end ----------



# ---------- DELETE MATERIAL start ----------

@materials_settings_router.message(AdminFilter(), F.text == 'Удалить материал')
async def del_material_start(message: Message, state: FSMContext):
    await state.set_state(DeleteMaterial.name)
    await message.answer("Выберите материал:", reply_markup=builder.get_materials_kb())
    
    
@materials_settings_router.callback_query(DeleteMaterial.name)
async def del_material_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.data)
    await state.set_state(DeleteMaterial.confirmation)
    await callback.message.edit_text("Вы уверены, что хотите удалить этот материал?", 
                                  reply_markup=inl.confirm)
    
    
@materials_settings_router.callback_query(DeleteMaterial.confirmation)
async def del_material_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        name = data.get("name")
        await del_material(name)
        await callback.message.answer(f"Материал '{name}' успешно удален!")
        await builder.update_materials_kb()
    else:
        await callback.message.answer("Действие отменено")
    await callback.message.delete()
    await state.clear()
    
# ---------- DELETE MATERIAL end ----------