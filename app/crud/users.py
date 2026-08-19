from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import User

async def get_or_create_user(
    session: AsyncSession, 
    telegram_id: int, 
    username: str | None = None, 
    first_name: str | None = None
) -> User:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none() 

    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user