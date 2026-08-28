from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.dialects.postgresql import insert

from app.db.base import User
from app.db.session import AsyncSessionLocal

router = Router()

@router.message(CommandStart())
async def command_start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    async with AsyncSessionLocal() as session:
        statement = insert(User).values(id=tg_id, telegram_id=tg_id, username=username)
        
        await session.execute(statement)
        await session.commit()
        
    await message.answer(
        f"Hello, {message.from_user.first_name}! 👋\n\n"
        "I'm a bot tracking cheap KTZ train tickets.\n\n"
        "Available commands:\n"
        "• /new_tracking — Create a new tracking\n"
        "• /my_trackings — My active trackings"
        )
        
        
    
    