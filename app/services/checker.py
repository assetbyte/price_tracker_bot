# parser with crud
from datetime import date
from decimal import Decimal
from typing import Optional
from app.services.cache_service import get_cache_ktzh_trains
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.notifier import send_tg_notification
from app.crud.price_history import get_latest_price_record
from app.crud.add_price_record import add_price_record
from app.db.base import Tracking
from app.scrapers.ktzh_client import get_ktzh_trains

from app.db.session import AsyncSessionLocal


async def process_tracking_checking(
    session: AsyncSession,
    tracking_info: Tracking,
) -> tuple[bool, Optional[Decimal]]:
    parsed_data = await get_cache_ktzh_trains(
        departure_code=tracking_info.origin_code,
        arrival_code=tracking_info.destination_code,
        departure_date=str(tracking_info.departure_date)
    )
    
    if not parsed_data: 
        return False, None
    
    last_record = await get_latest_price_record(
        session=session, 
        tracking_id=tracking_info.id
    )
    
    last_recorded_price = last_record.price if last_record else None
    
    tickets = parsed_data.get("tickets", [])
    if not tickets:
        return False, None

    if tracking_info.car_type:  # указан класс транспорта
        tickets = [ticket for ticket in tickets if ticket.get("car_type") == tracking_info.car_type]

    if not tickets:
        return False, None

    min_price_ticket = min(tickets, key=lambda ticket: ticket["price"])
    current_price = min_price_ticket["price"]

    await add_price_record(
        session=session,
        tracking_id=tracking_info.id,
        price=current_price
    )

    notification = current_price <= tracking_info.target_price
        
    return notification, current_price


async def run_all_price_checks() -> None: 
    async with AsyncSessionLocal() as session: 
        statement = select(Tracking).where(Tracking.is_active.is_(True))
        result = await session.execute(statement)
        active_trackings = result.scalars().all()
        
        if not active_trackings:
            print("No active trackings")
            return
            
        print(f"Launch checking for {len(active_trackings)} trackings")
        
        for tracking in active_trackings:
            try:
                should_notify, current_price = await process_tracking_checking(
                    session=session,
                    tracking_info=tracking
                )
                
                if should_notify:
                    message= (
                        f"<b>Good price tickets found!</b>\n\n"
                        f"Route: {tracking.origin_code} to {tracking.destination_code}\n"
                        f"Date: {tracking.departure_date}\n"
                        f"Target price: {tracking.target_price} ₸\n"
                        f"Current price: {current_price} ₸\n"
                    )
                    await send_tg_notification(
                        chat_id=tracking.user_id,
                        text=message
                    )
                    
        
            except Exception as e:
                print("Error", e)
        
    
    
    
    
    