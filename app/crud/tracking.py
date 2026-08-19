from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import Tracking 

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
