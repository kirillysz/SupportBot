from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import TOKEN
from handlers import admin_panel, user_commands, user_messages

import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup(dp):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота")
        ]
    )

async def main():
    dp.include_routers(
        user_commands.router,
        user_messages.router,
        admin_panel.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())