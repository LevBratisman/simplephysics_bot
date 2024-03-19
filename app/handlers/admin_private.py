from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.reply import get_keyboard
from app.filters.admin import IsAdmin
from app.filters.chat_type import ChatTypeFilter

admin_private_router = Router()
admin_private_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
admin_private_router.callback_query.filter(ChatTypeFilter(['private']), IsAdmin())


######################### КЛАВИАТУРЫ ###############################################

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    "Выйти из админ панели",
    placehoder="Выберите действие",
    sizes=(2, 1)
)

state_process_kb = get_keyboard(
    "Назад",
    "Отмена",
    placehoder="Выберите действие"
)

#########################################################################################


@admin_private_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("Вы зашли в админ панель", reply_markup=ADMIN_KB)
    
    
@admin_private_router.message(F.text=="Выйти из админ панели")
async def leave_admin_panel(message: Message):
    await message.answer("Вы вышли из админ панели", reply_markup=ReplyKeyboardRemove())

    
#########################################################################################



######################### FSM для дабавления/изменения товаров админом ##################

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    
    texts = {
        "AddProduct:name": "Введите название заново:",
        "AddProduct:description": "Введите описание заново:",
        "AddProduct:category": "Выберите категорию  заново ⬆️",
        "AddProduct:price": "Введите стоимость заново:",
        "AddProduct:image": "Этот стейт последний, поэтому...",
    }
    
    
@admin_private_router.message(StateFilter(None), F.text=="Добавить товар")
async def add_product(message: Message, state: FSMContext):
    await state.set_state(AddProduct.name)
    await message.answer("Введите название", reply_markup=state_process_kb)
    
    
@admin_private_router.message(StateFilter('*'), F.text.casefold()=="отмена")
async def reset_state(message: Message, state: FSMContext):
    
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)
    
    
@admin_private_router.message(StateFilter('*'), F.text.casefold()=="назад")
async def get_back(message: Message, state: FSMContext):
    
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer("Предыдущего шага нет. Введите название товара или напишите 'отмена'")
        return
    
    previous_state = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state)
            await message.answer(f'Вы вернулись назад. {AddProduct.texts[previous_state]}')
            return
        else:
            previous_state = step
    
    
@admin_private_router.message(AddProduct.name, F.text)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание")
    await state.set_state(AddProduct.description)
    
    
@admin_private_router.message(AddProduct.description, F.text)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Напишите цену")
    await state.set_state(AddProduct.price)
    
    
@admin_private_router.message(AddProduct.price, F.text)
async def get_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение")
    await state.set_state(AddProduct.image)
    
    
@admin_private_router.message(AddProduct.image, F.photo)
async def get_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(data["image"],
                               caption=f"Название: {data['name']}\nОписание: {data['description']}\nЦена: {data['price']}")
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    await state.clear()