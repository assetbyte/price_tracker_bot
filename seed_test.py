import asyncio
from datetime import date, timedelta
import random

from app.db.session import AsyncSessionLocal
from app.db.base import Tracking  # Перепроверьте импорт вашей модели Tracking

# Тестовые маршруты
ROUTES = [
    ("Астана", "Алматы"),
    ("Алматы", "Шымкент"),
    ("Атырау", "Астана"),
    ("Караганда", "Алматы"),
    ("Павлодар", "Астана"),
]

CLASSES = ["Плацкарт", "Купе", "Люкс (СВ)"]

async def seed_trackings():
    async with AsyncSessionLocal() as session:
        new_trackings = []
        today = date.today()

        # 1. Рабочие трекинги на будущие даты (нормальные кейсы)
        for i in range(8):
            origin, dest = random.choice(ROUTES)
            departure = today + timedelta(days=random.randint(1, 20))
            tracking = Tracking(
                user_id=1,  # Укажите ваш telegram/user_id
                route=f"{origin} ➔ {dest}",
                departure_date=departure,
                target_price=float(random.randint(8000, 25000)),
                train_class=random.choice(CLASSES),
                is_active=True,
            )
            new_trackings.append(tracking)

        # 2. Просроченные трекинги (для проверки Celery-задачи очистки)
        for i in range(4):
            origin, dest = random.choice(ROUTES)
            past_date = today - timedelta(days=random.randint(1, 10))
            tracking = Tracking(
                user_id=1,  # Укажите ваш telegram/user_id
                route=f"{origin} ➔ {dest}",
                departure_date=past_date,
                target_price=float(random.randint(5000, 15000)),
                train_class=random.choice(CLASSES),
                is_active=True,  # Пока True, чтобы очистка деактивировала их
            )
            new_trackings.append(tracking)

        session.add_all(new_trackings)
        await session.commit()
        print(f"Успешно создано {len(new_trackings)} тестовых трекингов!")

if __name__ == "__main__":
    asyncio.run(seed_trackings())