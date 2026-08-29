import asyncio
from aiogram import Bot, Dispatcher
from app.bot.handlers import start, tracking
from dotenv import load_dotenv
import os
load_dotenv()


async def main():
  bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
  dp = Dispatcher()

  dp.include_router(start.router)
  dp.include_router(tracking.router)

  print("Bot started")
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())