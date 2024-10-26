from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from data.database import Database
from keyboards.reply import question_kb
from keyboards.inline import admin_kb
from config import ADMIN_IDS, HOST

router = Router()
db = Database(host=HOST)

@router.message(CommandStart())
async def greeting(message: Message):
    user_id = str(message.from_user.id)
    
    if user_id in ADMIN_IDS.split(","):
        await message.answer(f"Приветствую, {message.from_user.full_name}!\nДавай работать.",
                                reply_markup=admin_kb)
        
    else:
        banned_user = await db.get_banned_users(user_id=user_id)

        if banned_user is None:
            await message.answer(
                f"Здравствуйте, {message.from_user.full_name}!\n"
                "Добро пожаловать в Бота-поддержку Univer's Project\n",
                reply_markup=question_kb
            )
            await db.add_user(user_id=user_id)
        else:
            await message.answer("Вы забанены в этом боте за нарушение правил.")
