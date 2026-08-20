from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import Tracking
from datetime import date
from decimal import Decimal
from typing import Optional

async def get_active_tracking(
    session: AsyncSession,
    user_id: int,
    origin_code: str,
    destination_code: str,
    departure_date: str,
    transport_type: str,
) -> Tracking: 
    result = await session.execute(
        select(Tracking).where(
            Tracking.user_id == user_id,
            Tracking.origin_code == origin_code,
            Tracking.destination_code == destination_code,
            Tracking.departure_date == departure_date,
            Tracking.transport_type == transport_type,
            Tracking.is_active.is_(True),
            
        )
    )
    return result.scalar_one_or_none()


async def create_tracking(
    session: AsyncSession,
    user_id: int,
    origin_code: str,
    destination_code: str,
    origin_name: str,
    destination_name: str,
    departure_date: date,
    transport_type: str,
    route: str,
    price: Decimal | float,
    target_price: Decimal | float,
    car_type: Optional[str] = None,
) -> Tracking:
    new_tracking = Tracking(
        user_id=user_id,
        origin_code=origin_code,
        destination_code=destination_code,
        origin_name=origin_name,
        destination_name=destination_name,
        departure_date=departure_date,
        transport_type=transport_type,
        route=route,
        price=price,
        target_price=target_price,
        car_type=car_type,
    )
    session.add(new_tracking)
    await session.commit()
    await session.refresh(new_tracking)

    return new_tracking
