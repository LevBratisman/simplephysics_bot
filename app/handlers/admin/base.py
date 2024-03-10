from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.filters import AdminFilter
from app.database.dao import get_users_all

from app.keyboards import reply as rp
from app.keyboards import inline as inl

admin_router = Router()


class SendAll(StatesGroup):
    text = State()
    photo_confirm = State()
    photo = State()
    confirmation = State()

    
# -------- Base commands --------

@admin_router.message(AdminFilter(), F.text == 'Админ панель')
async def to_admin_panel(message: Message):
    await message.answer("Вы вошли в админ-панель", reply_markup=rp.admin_panel)


@admin_router.message(AdminFilter(), F.text == 'Назад')
async def leave_admin_panel(message: Message, state: FSMContext):
    await message.answer("Вы вышли из админ-панели", reply_markup=rp.start_admin)
    await state.clear()
    

@admin_router.message(AdminFilter(), F.text == 'Сбросить')
async def reset_admin(message: Message, state: FSMContext):
    await message.answer("Сброс выполнен", reply_markup=rp.admin_panel)
    await state.clear()
    
    
# ----------------SENDALL start-----------------

@admin_router.message(AdminFilter(), F.text == 'Сделать рассылку')
async def sendall_start(message: Message, state: FSMContext):
    await state.set_state(SendAll.text)
    await message.answer("Напишите текст рассылки")
    
    
@admin_router.message(SendAll.text)
async def sendall_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(SendAll.photo_confirm)
    await message.answer("Хотите прикрепить фото к рассылке?", reply_markup=inl.confirm)
    
    
@admin_router.callback_query(SendAll.photo_confirm)
async def sendall_photo_confirm(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        await state.update_data(photo_confirm=True)
        await state.set_state(SendAll.photo)
        await callback.message.answer("Отправьте фото")
    else:
        await state.update_data(photo_confirm=False)
        await state.set_state(SendAll.confirmation)
        
        data = await state.get_data()
        await callback.message.answer(data.get("text"))
        await callback.message.answer("Вы точно хотите отправить эту рассылку?", 
                            reply_markup=inl.confirm_sendall)
        
    await callback.message.delete()


@admin_router.message(SendAll.photo)
async def sendall_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(SendAll.confirmation)
    data = await state.get_data()
    await message.answer_photo(data.get("photo"), caption=data.get("text"))
    await message.answer("Вы точно хотите отправить эту рассылку?", 
                         reply_markup=inl.confirm_sendall)
    
    
@admin_router.callback_query(SendAll.confirmation)
async def sendall_confirmation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "sendall":
        users = await get_users_all()
        data = await state.get_data()
        await callback.message.answer("Рассылка началась")
        
        if data.get("photo_confirm"):
            for user in users:
                await bot.send_photo(user[1], photo=data.get("photo"), caption=data.get("text"))
        else:
            for user in users:
                await bot.send_message(user[1], data.get("text"))
                
        await callback.message.answer("Рассылка завершена")
    else:
        await callback.message.answer("Рассылка отменена")
    await callback.message.delete()
    await state.clear()
    
# ----------------SENDALL end-----------------