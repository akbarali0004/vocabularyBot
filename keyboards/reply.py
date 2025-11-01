from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/cancel")
        ]
    ], resize_keyboard=True
)