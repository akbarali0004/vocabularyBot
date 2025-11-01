from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📚 Add Word', callback_data='add_word'),
        ],
        [
            InlineKeyboardButton(text="📋 My Words", callback_data='view_words')
        ],
        [
            InlineKeyboardButton(text="📊 My stats", callback_data='stats')
        ]
    ]
)


menu2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Start quiz", callback_data="start_quiz")
        ],
        [
            InlineKeyboardButton(text="Menu", callback_data="main_menu")
        ]
    ]
)

direction_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖 English → 👤 Uzbek", callback_data="eng_uz")
        ],
        [
            InlineKeyboardButton(text="🤖 Uzbek → 👤 English", callback_data="uz_eng")
        ]
    ]
)

ready_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ I’m ready", callback_data="ready")
        ]
    ]
)


stop_quiz_btn = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔁 Try Again", callback_data="retry_quiz")
        ],
        [
            InlineKeyboardButton(text="📤 Share Quiz", callback_data="share_quiz")
        ],
        [
            InlineKeyboardButton(text="📋 My Words", callback_data="view_words")
        ]
    ]
)


def view_categories_btn(categories):
    btn = []
    for item in categories:
        btn.append([InlineKeyboardButton(text=f"{item[1]}", callback_data=f"cat_{item[0]}")])

    return InlineKeyboardMarkup(inline_keyboard=btn)