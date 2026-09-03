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
from app.services.checker import process_tracking_checking

router = Router()

@router.message(Command("my_trackings"))
async def my_trackings(message: types.Message):
    tg_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        statement = select(Tracking).join(User).where(User.telegram_id == tg_id).order_by(Tracking.created_at.desc())
        result = await session.execute(statement)
        trackings = result.scalars().all()
        
        if not trackings:
            await message.answer('For now you dont have any trackings. For create one you can use /new_tracking command')
            return
    await message.answer(" <b>Your active trackings: </b>", parse_mode="HTML")
    
    for elem in trackings:
        text = (
            f"<b>Tracking ID:</b> {elem.id}\n"
            f"<b>Route:</b> {elem.origin_name} ➔ {elem.destination_name}\n"
            f"<b>Departure date:</b> {elem.departure_date}\n"
            f"<b>Target price:</b> {elem.target_price} ₸\n"
            f"<b>Class/Type:</b> {elem.car_type or 'Any'}\n"
        )
        
        
        await message.answer(text, parse_mode="HTML")
        