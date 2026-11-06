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
from app.bot.handlers.tracking import FormEditTracking
router = Router()
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@router.message(Command("my_trackings"))
async def my_trackings(message: types.Message):
    tg_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        statement = (
            select(Tracking)
            .join(User)
            .where(User.telegram_id == tg_id)
            .order_by(Tracking.created_at.desc())
        )
        result = await session.execute(statement)
        trackings = result.scalars().all()
        
        if not trackings:
            await message.answer(
                "For now you don't have any trackings. "
                "To create one, use the /new_tracking command."
            )
            return

    await message.answer("📋 <b>Your active trackings:</b>", parse_mode="HTML")
    
    for elem in trackings:
        text = (
            f"<b>ID:</b> {elem.id}\n"
            f"<b>Route:</b> {elem.origin_name} ➔ {elem.destination_name}\n"
            f"<b>Date:</b> {elem.departure_date}\n"
            f"<b>Target price:</b> {elem.target_price} ₸\n"
            f"<b>Car class:</b> {elem.car_type or 'Any'}\n"
        )
        
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Delete tracking", 
                    callback_data=f"delete_tracking_{elem.id}"
                ),
                InlineKeyboardButton(text="Edit tracking", callback_data=f"edit_tracking_{elem.id}")
            ]]
        )
        
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)



@router.callback_query(F.data.startswith("delete_tracking_"))
async def process_delete_tracking(callback: types.CallbackQuery):
    # "delete_tracking_15" -> 15
    tracking_id = int(callback.data.split("_")[2])
    tg_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        statement = (select(Tracking).join(User)
            .where(Tracking.id == tracking_id, User.telegram_id == tg_id)
        )
        result = await session.execute(statement)
        tracking = result.scalar_one_or_none()

        if tracking:
            await session.delete(tracking)
            await session.commit()
            
            await callback.message.edit_text(
                f"{callback.message.html_text}\n\n<i>[Deleted]</i>",
                parse_mode="HTML"
            )
            await callback.answer("Tracking successfully deleted!")
        else:
            await callback.answer("Tracking not found or already deleted.", show_alert=True)
            
            
@router.callback_query(F.data.startswith("edit_tracking_"))
async def process_edit_tracking(callback: types.CallbackQuery, state: FSMContext):
    tracking_id = int(callback.data.split("_")[2])
    tg_id = callback.from_user.id #button click
    
    async with AsyncSessionLocal() as session: 
        statement = select(Tracking).join(User).where(Tracking.id == tracking_id, User.telegram_id == tg_id)
        result = await session.execute(statement)
        tracking = result.scalar_one_or_none()
        
        
        if not tracking: 
            await callback.answer(f"Such tracking not found!", show_alert=True)
        
        await state.update_data(editing_tracking_id = tracking.id)
        
        await state.set_state(FormEditTracking.origin)
            
        await callback.message.answer(
            f"Editing tracking #{tracking.id} "
            f"({tracking.origin_name} ➔ {tracking.destination_name}).\n\n"
            f"Enter new departure station name:",
            parse_mode="HTML"
        )
        await callback.answer()