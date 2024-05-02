import asyncio, os

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.dao import get_video_by_name
from app.keyboards import reply as rp
from app.keyboards import inline as inl
from app.keyboards import builder


from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

video_router = Router()


class Videos(StatesGroup):
    video = State()
    to_menu = State()


# ------------ GET VIDEOS start ----------

@video_router.message(F.text == '🎥Видео-контент')
async def get_videos_start(message: Message, state: FSMContext):
    await state.set_state(Videos.video)
    keyboard = builder.get_videos_kb()
    if not keyboard:
        await message.answer("Пусто...")
        await state.clear()
        return
    await message.answer("Подгружаю видео...", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.7)
    await message.answer("Готово! Выбирайте:", 
                         reply_markup=builder.get_videos_kb())
    
    
@video_router.callback_query(Videos.video)
async def choose_video(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == '⬅️Вернуться к меню':
        await callback.answer(f'Меню') 
        await state.clear()
        await callback.message.delete()
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start_admin)
        else:
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start)
    else:
        await callback.answer(f'{callback.data}')
        await state.update_data(video=callback.data)
        await state.set_state(Videos.to_menu)
        await callback.message.delete()
        
        video = await get_video_by_name(callback.data)
        await bot.send_video(chat_id=callback.message.chat.id, 
                             video=video[2], 
                             caption=video[3], 
                             reply_markup=inl.back)
        
        
@video_router.callback_query(Videos.to_menu)
async def get_video_to_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_menu':
        await callback.answer(f'Меню') 
        await state.clear()
        await callback.message.delete()
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start_admin)
        else:
            await callback.message.answer("Вы вернулись в главное меню", 
                                         reply_markup=rp.start)
    elif callback.data == 'back':
        await state.set_state(Videos.video)
        await callback.message.delete()
        await callback.answer('Видео-контент')
        await callback.message.answer("Выберите видео:", reply_markup=builder.get_videos_kb())
        

