from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.filters import AdminFilter
from app.database.dao import add_video, del_video_by_name
from app.keyboards import builder

from app.keyboards import reply as rp
from app.keyboards import inline as inl

video_settings_router = Router()


class AddVideo(StatesGroup):
    name = State()
    video = State()
    caption = State()
    confirmation = State()
    

class DeleteVideo(StatesGroup):
    name = State()
    confirmation = State() 


# ---------- ADD VIDEO start ----------

@video_settings_router.message(AdminFilter(), F.text == 'Добавить видео')
async def add_video_start(message: Message, state: FSMContext):
    await state.set_state(AddVideo.name)
    await message.answer("Напишите название видео")
    
    
@video_settings_router.message(AddVideo.name, F.text)
async def add_video_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddVideo.video)
    await message.answer("Отправьте видео")
    
    
@video_settings_router.message(AddVideo.video, F.video)
async def add_video_content(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await state.set_state(AddVideo.caption)
    await message.answer("Введите описание")
    
    
@video_settings_router.message(AddVideo.caption, F.text)
async def add_video_caption(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await state.set_state(AddVideo.confirmation)
    await message.answer("Вы уверены, что хотите добавить этот видео?", 
                         reply_markup=inl.confirm)
    
    
@video_settings_router.callback_query(AddVideo.confirmation)
async def add_video_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        name = data.get("name")
        video = data.get("video")
        caption = data.get("caption")
        await add_video(name, video, caption)
        await callback.message.edit_text("Видео добавлено!")
        await builder.update_videos_kb()
    else:
        await callback.message.edit_text("Видео не добавлено!")
    await state.clear()
    
# ---------- ADD MATERIAL end ----------



# ---------- DELETE VIDEO start ----------

@video_settings_router.message(AdminFilter(), F.text == 'Удалить видео')
async def del_video_start(message: Message, state: FSMContext):
    await state.set_state(DeleteVideo.name)
    await message.answer("Выберите видео:", reply_markup=builder.get_videos_kb())
    
    
@video_settings_router.callback_query(DeleteVideo.name)
async def del_video_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.data)
    await state.set_state(DeleteVideo.confirmation)
    await callback.message.edit_text("Вы уверены, что хотите удалить это видео?", 
                                  reply_markup=inl.confirm)
    
    
@video_settings_router.callback_query(DeleteVideo.confirmation)
async def del_video_confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        name = data.get("name")
        await del_video_by_name(name)
        await callback.message.answer(f"Видео '{name}' успешно удалено!")
        await builder.update_videos_kb()
    else:
        await callback.message.answer("Действие отменено")
    await callback.message.delete()
    await state.clear()
    
# ---------- DELETE MATERIAL end ----------