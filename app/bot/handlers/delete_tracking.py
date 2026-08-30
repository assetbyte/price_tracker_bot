from datetime import datetime
from decimal import Decimal
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from app.services.checker import run_all_price_checks
from app.db.base import Tracking, User 
from app.db.session import AsyncSessionLocal
from sqlalchemy import delete

router = Router()

@router.message(Command("delete_all_trackings"))
async def delete_trackings(message: types.Message):
    tg_id = message.from_user.id
    
    async with AsyncSessionLocal() as session: 
        statement = select(User).where(User.telegram_id == tg_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        
        if user:
            stmt = delete(Tracking).where(Tracking.user_id == user.id)
            
            await session.execute(stmt)
            await session.commit()
            await message.answer("All trackings were deleted successfully")
            
        else: await message.answer("No user found")
            
            