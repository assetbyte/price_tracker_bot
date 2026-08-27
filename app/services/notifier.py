from aiogram import Bot
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_tg_notification(chat_id: int, text: str) -> None:
    bot = Bot(token=token)
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML"
        )
        
    finally:
        await bot.session.close()
    