from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

question_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задать вопрос ✏")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)