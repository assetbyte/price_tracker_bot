from app.db.base import Station
from app.db.session import AsyncSessionLocal
from sqlalchemy import case, func, select


async def fuzzy_search_station(query: str): 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Station)
            .where(~Station.name.contains("->"))  
            .order_by(
                case((Station.is_popular == True, 1), else_=0).desc(),
                func.similarity(Station.name, query).desc()
            )
            .limit(5)
        )
        return result.scalars().all()