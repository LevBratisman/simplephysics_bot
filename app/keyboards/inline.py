from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])


confirm_sendall = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отправить всем", callback_data="sendall"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])