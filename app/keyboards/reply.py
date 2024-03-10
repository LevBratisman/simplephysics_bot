from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Start menu
start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Материалы")
        ],
        [
            KeyboardButton(text="Информация о боте")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

# Start menu for admin
start_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Материалы")
        ],
        [
            KeyboardButton(text="Информация о боте")
        ],
        [
            KeyboardButton(text="Админ панель")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)


# Admin panel
admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить материал"),
            KeyboardButton(text="Удалить материал")
        ],
        [
            KeyboardButton(text="Добавить документ"),
            KeyboardButton(text="Удалить документ")
        ],
        [
            KeyboardButton(text="Сделать рассылку"),
            KeyboardButton(text="Статистика")
        ],
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="Сбросить")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие.'
)