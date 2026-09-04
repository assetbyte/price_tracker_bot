import asyncio
from aiogram import Bot, Dispatcher
from app.bot.handlers import delete, start, tracking, view, common
from dotenv import load_dotenv
from aiogram.types import BotCommand, BotCommandScopeDefault
import os
load_dotenv()

async def set_bot_commands(bot: Bot):
  commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="new_tracking", description="Create a new price tracking"),
    BotCommand(command="delete_specific_tracking", description="Delete a specific price tracking by its ID"),
    BotCommand(command="edit_tracking", description="Edit a specific price tracking by its ID"),
    BotCommand(command="check_now", description="Check prices immediately"),
    BotCommand(command="my_trackings", description="View all your price trackings"),
    BotCommand(command="delete_all_trackings", description="Delete all your price trackings"),
    BotCommand(command="help", description="Get help"),
    BotCommand(command="cancel", description="Cancel the current action"),
  ]
  await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def main():
  bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
  dp = Dispatcher()
  dp.include_router(common.router)
  dp.include_router(start.router)
  dp.include_router(tracking.router)
  dp.include_router(view.router)
  dp.include_router(delete.router)
  print("Bot started")
  
  await set_bot_commands(bot)
  await dp.start_polling(bot)
  


if __name__ == "__main__":
  asyncio.run(main())