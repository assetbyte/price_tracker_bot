import asyncio
from datetime import date
from app.db.session import AsyncSessionLocal
from app.db.base import User, Tracking 

async def create_test_tracking():
    async with AsyncSessionLocal() as session:
        user_id = 1847520791
        
        user = await session.get(User, user_id)
        if not user:
            user = User(
                id=user_id,
                telegram_id=user_id, 
                username="test_user"
            )
            session.add(user)
            await session.flush() 

        test_tracking = Tracking(
            user_id=user.id,
            origin_code="2700000",
            destination_code="2708001",
            origin_name="Астана",
            destination_name="Алматы",
            departure_date=date(2026, 8, 31),
            target_price=999999,
            transport_type="train",
            car_type="Купе",
            is_active=True
        )
        session.add(test_tracking)
        
        await session.commit()
        print(f"Tracking created, id: {test_tracking.id}")

if __name__ == "__main__":
    asyncio.run(create_test_tracking())