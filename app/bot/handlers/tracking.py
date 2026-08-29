from datetime import datetime
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from app.db.base import Tracking, User 
from app.db.session import AsyncSessionLocal

router = Router()


class FormTracking(StatesGroup):
  origin = State()
  destination = State()
  departure_date = State()
  car_type = State()
  target_price = State()


async def get_station_code(station_name: str) -> str:
  # test variant
  return "2700000"


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
        target_price = float(message.text.strip().replace(",", "."))
        
        if target_price <=0 :
            await message.answer("Price must be greater than 0")
            return
        
        user = await state.get_data()
        telegram_id = message.from_user.id
        async with AsyncSessionLocal() as session:
            statement = select(User).where(User.telegram_id==telegram_id)
            result = await session.execute(statement)
            db_user = result.scalar_one_or_none()
            
            if not db_user:
                await message.answer("User not found")
                await state.clear()
                return
            new_tracking = Tracking(
                user_id=db_user.id,  
                origin_code=user["origin_code"],
                destination_code=user["destination_code"],
                origin_name=user["origin_name"],
                destination_name=user["destination_name"],
                departure_date=user["departure_date"],
                target_price=target_price,
                car_type=user["car_type"],
                transport_type="train",
                is_active=True,
            )
            session.add(new_tracking)
            await session.commit()
            
            await state.clear()
            await message.answer("Tracking successfully created")
            
    except ValueError:
        await message.answer(
            "Invalid price format")
        
        

