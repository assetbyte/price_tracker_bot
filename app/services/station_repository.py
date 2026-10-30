from app.db.base import Station
from app.db.session import AsyncSessionLocal
from sqlalchemy import func, select


async def fuzzy_search_station(query: str): 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Station)
            .order_by(func.similarity(Station.name, query).desc())
            .limit(5)  
        )
        return result.scalars().all()