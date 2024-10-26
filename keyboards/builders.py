from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

async def build_questions(questions):
    builder = InlineKeyboardBuilder()

    for question in questions:
        question_text = question.get('question')
        if len(question_text) > 15:
            question_text = f"{question_text[:15]}..."
        
        builder.row(InlineKeyboardButton(text=question_text, callback_data=f"question_{question['user_id']}"),
                    width=1)

    return builder.as_markup()

async def build_ban(users):
    builder = InlineKeyboardBuilder()

    for user in users:
        user_id = user.get("user_id")

        builder.row(InlineKeyboardButton(text=str(user_id), callback_data=f"ban_{user_id}"),
                    width=1)

    return builder.as_markup()
