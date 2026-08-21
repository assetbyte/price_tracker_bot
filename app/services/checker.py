# parser with crud
from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.price_history import add_price_record, get_latest_price_record
from app.db.base import Tracking
from scrapers.ktzh_client import get_ktzh_trains


async def process_tracking_checking(
    session: AsyncSession,
    tracking_info: Tracking,
) -> bool:
    # 1. Вызываем асинхронный парсер
    parsed_data = await get_ktzh_trains(
        departure_code=tracking_info.origin_code,
        arrival_code=tracking_info.destination_code,
        departure_date=str(tracking_info.departure_date)
    )
    
    if not parsed_data: 
        return False
    
    last_record = await get_latest_price_record(
        session=session, 
        tracking_id=tracking_info.id
    )
    
    last_recorded_price = last_record.price if last_record else None
    
    notification = False
    # "tickets": [
    #     {
    #         "car_type": "Купе",
    #         "free_seats": 15,
    #         "price": 14513
    #     }
    # ]

    tickets = parsed_data["tickets"]
    
    min_price_ticket = min(tickets, key=lambda ticket: ticket["price"]) # пока без учета вида транспорта
    
    
    
    if min_price_ticket["price"] <= tracking_info.target_price:
        notification = True
        
        
    await add_price_record(
                session=session,
                tracking_id=tracking_info.id,
                price=min_price_ticket["price"]
            )
        
        
    return notification