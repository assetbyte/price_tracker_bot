import os
from typing import AsyncGenerator 
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True,)

AsyncSessionLocal = async_sessionmaker (
    bind = engine, # 1 юзер = 1 сессия, 1 сессия = 1 транзакция
    class_=AsyncSession, # асинхронная сессия
    expire_on_commit=False, # нужно чтобы после коммита объекты не теряли свои значения
    autoflush= False,   #  лишний раз не отправлять изменения в базу данных, пока не вызван commit
    autocommit = False, # автоматически не коммитить изменения в базу данных, пока не вызван commit
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]: # на выход = AsyncSession, на вход = None
    async with AsyncSessionLocal() as session: 
        yield session # полностью не завершает сессию, а только передает управление вызывающему коду, который может использовать сессию для выполнения операций с базой данных



