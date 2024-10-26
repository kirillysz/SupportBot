from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from data.database import Database
from forms.forms import AnswerForm
from config import HOST

from keyboards.builders import build_questions, build_ban
from keyboards.inline import admin_kb, admin_panel_kb
from keyboards.reply import question_kb

router = Router()
db = Database(host=HOST)

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    await callback.message.answer("...", reply_markup=admin_panel_kb)

@router.callback_query(F.data == "answer_the_questions")
async def questions(callback: CallbackQuery):
    questions = await db.get_all_questions()

    if questions:
        keyboard = await build_questions(questions=questions)

        await callback.message.delete()
        await callback.message.answer("Список вопросов",
                                    reply_markup=keyboard)
    else:
        await callback.message.delete()
        await callback.message.answer("Вопросов пока-что нет.")

    await callback.answer()


@router.callback_query(F.data.startswith("question_"))
async def handle_question(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.data.split("_")[1])

    question_dict = await db.get_question_by_id(user_id=user_id)
    question = question_dict.get('question')
    
    await callback.message.answer(f"Отлично, выбран вопрос пользователя `{user_id}`: `{question}`\nЖду ответ",
                                parse_mode="MARKDOWN")

    await state.update_data({"question_user_id": user_id, "question": question})
    await state.set_state(AnswerForm.answer)

@router.message(AnswerForm.answer)
async def result(message: Message, state: FSMContext):
    from main import bot

    await state.update_data({"answer": message.text})
    data = await state.get_data()
    
    answer = data.get("answer")
    question_user_id = data.get("question_user_id")
    question = data.get("question")
    
    await bot.send_message(question_user_id, f"На ваш вопрос: `{question}` ответил наш помошник.\n"
                           f"Вот его ответ:\n`{answer}`",
                           parse_mode="MARKDOWN",
                           reply_markup=question_kb)

    await db.answer_the_question(user_id=question_user_id)

    try:
        await message.answer("Ответ успешно был отправлен пользователю", 
                            reply_markup=admin_kb)
    except Exception as _err:
        await print(f"Не удалось отправить сообщение пользователю {question_user_id}: {_err}")


@router.callback_query(F.data == "_ban_person")
async def ban_user(callback: CallbackQuery):
    users = await db.get_users()

    await callback.message.delete()
    await callback.message.answer("Выбери пользователя, которого нужно забанить.",
                                reply_markup=await build_ban(users=users))

@router.callback_query(F.data.startswith("ban_"))
async def get_user_id_for_ban(callback: CallbackQuery):
    user_id_for_ban = str(callback.data.split("_")[1])
    try:
        await db.ban_user(user_id=user_id_for_ban)
        await callback.message.delete()
        await callback.message.answer("Пользотель успешно забанен.")
    except Exception as _err:
        print(f"Не удалось забанить пользователя {user_id_for_ban}: {_err}")