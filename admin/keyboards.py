from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Активные пользователи")
        ],
        [
            KeyboardButton(text="Найти информацию о пользователе")
        ],
        [
            KeyboardButton(text="Общая рассылка"),
            KeyboardButton(text="Личное сообщение")
        ]
    ],
    resize_keyboard=True
)

back_to_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="◀️ Вернуться в главное меню")
        ]
    ],
    resize_keyboard=True
)
