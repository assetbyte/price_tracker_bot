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

class FormDeleteTracking(StatesGroup):
    tracking_id = State()

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
        
        
@router.message(Command("delete_specific_tracking"))
async def start_delete_specific_tracking(message: types.Message, state: FSMContext):
    await state.set_state(FormDeleteTracking.tracking_id)
    await message.answer("Enter your tracking ID:")
    
    
@router.message(FormDeleteTracking.tracking_id)
async def process_tracking_id(message: types.Message, state: FSMContext):
    if not message.text.strip().isdigit():
        await message.answer("Please enter a valid ID (number)")
        return

    tracking_id = int(message.text.strip())
    tg_id = message.from_user.id
    try:
        async with AsyncSessionLocal() as session:
            statement = select(Tracking).join(User).where(Tracking.id == tracking_id, User.telegram_id == tg_id)
            result = await session.execute(statement)
            tracking = result.scalar_one_or_none()

            if tracking:
                await session.delete(tracking)
                await session.commit()
                await message.answer(f"Tracking with ID {tracking_id} was deleted successfully")
            else:
                await message.answer(f"No tracking found with ID {tracking_id}")

    except Exception as e:
        await message.answer(f"error: {str(e)}")
    finally:
        await state.clear()