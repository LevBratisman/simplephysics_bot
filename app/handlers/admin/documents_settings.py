from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.filters import AdminFilter
from app.database.dao import add_doc, del_doc, get_material_by_name
from app.keyboards import builder

from app.keyboards import reply as rp
from app.keyboards import inline as inl

documents_settings_router = Router()


class AddDocument(StatesGroup):
    catalog = State()
    name = State()
    document = State()
    confirmation = State()
    

class DeleteDocument(StatesGroup):
    catalog = State()
    name = State()
    confirmation = State() 


# ---------- ADD DOCUMENT start ----------

@documents_settings_router.message(AdminFilter(), F.text == 'Добавить документ')
async def add_document_start(message: Message, state: FSMContext):
    await state.set_state(AddDocument.catalog)
    await message.answer("Выберите каталог:", reply_markup=builder.get_materials_kb())
    
    
@documents_settings_router.callback_query(AddDocument.catalog)
async def add_document_catalog(callback: CallbackQuery, state: FSMContext):
    await state.update_data(catalog=callback.data)
    await state.set_state(AddDocument.name)
    await callback.message.answer("Введите название документа")
    
    
@documents_settings_router.message(AddDocument.name)
async def add_document_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddDocument.document)
    await message.answer("Отправьте документ")
    
    
@documents_settings_router.message(AddDocument.document)
async def add_document_document(message: Message, state: FSMContext):
    await state.update_data(document=message.document.file_id)
    await state.set_state(AddDocument.confirmation)
    await message.answer("Вы точно хотите добавить этот документ?", reply_markup=inl.confirm)
    
    
@documents_settings_router.callback_query(AddDocument.confirmation)
async def add_document_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        material = await get_material_by_name(data.get("catalog"))
        print(material)
        await add_doc(data.get("name"), material[0], data.get("document"))
        await callback.message.answer(f"Документ '{data.get('name')}' успешно добавлен в Каталог '{data.get('catalog')}'!")
        await builder.update_docs_kb()
    else:
        await callback.message.answer("Действие отменено")
    await callback.message.delete()
    await state.clear()
    
# ---------- ADD DOCUMENT end ----------



# ---------- DELETE DOCUMENT start ----------

@documents_settings_router.message(AdminFilter(), F.text == 'Удалить документ')
async def del_document_start(message: Message, state: FSMContext):
    await state.set_state(DeleteDocument.catalog)
    await message.answer("Выберите материал:", reply_markup=builder.get_materials_kb())
    
    
@documents_settings_router.callback_query(DeleteDocument.catalog)
async def del_document_catalog(callback: CallbackQuery, state: FSMContext):
    await state.update_data(catalog=callback.data)
    material = await get_material_by_name(callback.data)
    material_id = material[0]
    await state.set_state(DeleteDocument.name)
    await callback.message.edit_text("Выберите документ:", 
                                     reply_markup=builder.get_docs_kb(material_id))
    
    
@documents_settings_router.callback_query(DeleteDocument.name)
async def del_document_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.data)
    await state.set_state(DeleteDocument.confirmation)
    await callback.message.edit_text("Вы уверены, что хотите удалить этот документ?", 
                                     reply_markup=inl.confirm)
    
    
@documents_settings_router.callback_query(DeleteDocument.confirmation)
async def del_document_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        await del_doc(data.get("name"))
        await callback.message.answer(f"Документ '{data.get('name')}' успешно удален!")
        await builder.update_docs_kb()
    else:
        await callback.message.answer("Действие отменено")
    await callback.message.delete()
    await state.clear()
    
# ---------- DELETE DOCUMENT end ----------