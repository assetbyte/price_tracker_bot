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


async def get_latest_price_record(
    session: AsyncSession,
    tracking_id: int,
) -> PriceHistory | None:
    result = await session.execute(
        select(PriceHistory)
        .where(PriceHistory.tracking_id == tracking_id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


