from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from main import bot
from keyboards.inline import admin_kb
from keyboards.reply import question_kb

from forms.forms import QuestionForm
from data.database import Database
from config import HOST, ADMIN_IDS

router = Router()
db = Database(host=HOST)

@router.message(F.text == "Задать вопрос ✏")
async def process_question(message: Message, state: FSMContext):
    question = await db.get_question_by_id(user_id=message.from_user.id)

    if await db.get_banned_users(user_id=message.from_user.id) is None:
        if question is None:
            await state.set_state(QuestionForm.question)
            await message.answer(
                "Опишите вашу проблему.\n"
                "Для того, чтобы Помошник грамотно ответил на Ваш вопрос, пожалуйста, сформулируйте его корректно."
            )
        else:
            await message.answer(
                f"Вы уже отправили вопрос: `{question.get('question')}`.\n"
                "Пожалуйста, дождитесь ответа на него, прежде чем писать новый.",
                parse_mode="MARKDOWN"
            )
    else:
        await message.answer("Вы забанены в этом боте за нарушений правил.")

@router.message(QuestionForm.question)
async def result(message: Message, state: FSMContext):
    await state.set_data({"question": message.text})

    data = await state.get_data()
    question = data.get("question")

    await db.add_question(user_id=str(message.from_user.id), question=question)

    for admin_id in ADMIN_IDS.split(","):
        try:
            admin_id = int(admin_id.strip())
            await bot.send_message(
                admin_id,
                f"Пользователь `{message.from_user.id}` отправил вопрос: `{question}`",
                parse_mode="MARKDOWN",
                reply_markup=admin_kb
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение администратору {admin_id}: {e}")

    await message.reply("Приняли. Ваш вопрос уже отправлен нашим помощникам.")
    await state.clear()
