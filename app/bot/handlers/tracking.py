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
STATION_CHOICES = {
    "астана": "2700000",
    "алматы": "2708001",
}

class FormTracking(StatesGroup):
  origin = State()
  destination = State()
  departure_date = State()
  car_type = State()
  target_price = State()

from sqlalchemy import delete

async def get_station_code(station_name: str) -> str | None:
    clean_name = station_name.strip().lower()
    return STATION_CHOICES.get(clean_name)

@router.message(Command("new_tracking"))
async def start_tracking_creation(message: types.Message, state: FSMContext):
    await state.set_state(FormTracking.origin)
    await message.answer("Enter name of a departure station:")
    

@router.message(FormTracking.origin)
async def process_origin(message: types.Message, state: FSMContext):
    origin_name = message.text.strip()
    origin_code = await get_station_code(origin_name)
    await state.update_data(origin_name=origin_name, origin_code=origin_code)
    await state.set_state(FormTracking.destination)
    await message.answer("Enter name of the arrival station:")

@router.message(FormTracking.destination)
async def process_destination(message: types.Message, state: FSMContext):
    destination_name = message.text.strip()
    destination_code = await get_station_code(destination_name)
    
    await state.update_data(destination_name=destination_name, destination_code=destination_code)
    await state.set_state(FormTracking.departure_date)
    await message.answer('Enter departure date in "DD-MM-YYYY" format:')


@router.message(FormTracking.departure_date)
async def process_departure_date(message: types.Message, state: FSMContext):
    try: 
        parsed_date = datetime.strptime(message.text.strip(), "%d-%m-%Y").date()
        
        if parsed_date < datetime.now().date():
            await message.answer("Date cannot be in the past, enter a valid date!")
            return
        await state.update_data(departure_date=parsed_date)
        await state.set_state(FormTracking.car_type)
        await message.answer("Choose a train carriage type (Плацкарт, Купе, Люкс):")
    
    except ValueError:
        await message.answer('Invalid date, use "DD-MM-YYYY" format:')


@router.message(FormTracking.car_type)
async def process_car_type(message: types.Message, state: FSMContext):
    car_type = message.text.strip()
    await state.update_data(car_type=car_type)
    await state.set_state(FormTracking.target_price)
    await message.answer("Enter you desirable maximum price:")




@router.message(FormTracking.target_price)
async def process_target_price(message: types.Message, state: FSMContext):
    try:
        raw_price = message.text.strip().replace(",", ".")
        target_price = Decimal(raw_price)
        
        if target_price <= 0:
            await message.answer("Price must be greater than 0")
            return

        user_data = await state.get_data()
        telegram_id = message.from_user.id
        
        async with AsyncSessionLocal() as session:
            statement = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(statement)
            db_user = result.scalar_one_or_none()
            
            if not db_user:
                await message.answer("User not found")
                await state.clear()
                return
                
            new_tracking = Tracking(
                user_id=db_user.id,  
                origin_code=user_data["origin_code"],
                destination_code=user_data["destination_code"],
                origin_name=user_data["origin_name"],
                destination_name=user_data["destination_name"],
                departure_date=user_data["departure_date"],
                target_price=target_price,
                car_type=user_data["car_type"],
                transport_type="train",
                is_active=True,
            )
            session.add(new_tracking)
            await session.commit()
            await session.refresh(new_tracking)
            
            await state.clear()
            
            await message.answer("Tracking successfully created!")
            
            should_notify, current_price = await process_tracking_checking(
                session=session,
                tracking_info=new_tracking
            )
            
            if current_price is not None:
                if should_notify:
                    await message.answer(
                        f"<b>I found cheap tickets for you right now!</b>\n\n"
                        f"Route: {new_tracking.origin_name} ➔ {new_tracking.destination_name}\n"
                        f"Date: {new_tracking.departure_date}\n"
                        f"Current price: <b>{current_price} ₸</b>\n"
                        f"Your target: {target_price} ₸",
                        parse_mode="HTML"
                    )
                else:
                    await message.answer(
                        f"Current minimum price right now is <b>{current_price} ₸</b>.\n"
                        f"We will notify you when price drops to or below {target_price} ₸.",
                        parse_mode="HTML"
                    )
            else:
                await message.answer(
                    "Could not find active tickets for these parameters at the moment"
                )

    except ValueError:
        await message.answer("Invalid price format")