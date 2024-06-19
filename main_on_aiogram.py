import asyncio
from aiogram import Bot, Dispatcher
from true_handlers import router
from dotenv import load_dotenv
from os import getenv

load_dotenv()
bot = Bot(getenv("TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
