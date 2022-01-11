from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Когда нужно проснуться ☀️"), KeyboardButton(text="Когда нужно лечь спать 🛌")
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
