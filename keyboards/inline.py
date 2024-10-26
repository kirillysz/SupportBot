from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Админ Панель ⚙️", callback_data="admin_panel")
        ]
    ]
)


admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ответить на вопросы", callback_data="answer_the_questions"),
            InlineKeyboardButton(text="Забанить человека", callback_data="_ban_person")
        ]
    ]
)