from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.routers import router
import asyncio
import logging
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
