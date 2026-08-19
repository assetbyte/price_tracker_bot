from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import PriceHistory


async def get_price_history(
    session: AsyncSession,
    tracking_id: int,
) -> list[PriceHistory]: 
    result = await session.execute(
        select(PriceHistory).where(
            PriceHistory.tracking_id == tracking_id
        ).order_by(PriceHistory.recorded_at.asc())
    )
    
    return result.scalars().all() 