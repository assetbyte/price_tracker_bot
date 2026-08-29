from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import PriceHistory
from typing import Any, Optional
from datetime import datetime
from datetime import datetime, timezone

async def add_price_record(
    session: AsyncSession,
    tracking_id: int,
    new_price: float,
    carrier: str,
    details: Optional[dict[str, Any]] = None,
    time: Optional[datetime] = None
) -> PriceHistory:
    
    if time is None:
        time = datetime.now(timezone.utc)

    new_record = PriceHistory(
        tracking_id=tracking_id,
        price=new_price,
        carrier=carrier,
        details=details,
        time=time  
    )
    session.add(new_record)
    await session.commit()
    await session.refresh(new_record)
    return new_record