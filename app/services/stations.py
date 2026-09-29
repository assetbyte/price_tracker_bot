from app.db.base import Station
from app.db.session import AsyncSessionLocal
from sqlalchemy import select

async def get_station_code_by_name(name: str) -> str | None:
  async with AsyncSessionLocal() as session:
    clean_name = name.strip()
    statement = select(Station.code).where(Station.name.ilike(f"%{clean_name}%")).limit(1)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def get_popular_stations_from_db():
    async with AsyncSessionLocal() as session:
        statement = select(Station.name).where(Station.is_popular.is_(True))
        result = await session.execute(statement)
        popular_stations = list(result.scalars().all())
        return popular_stations