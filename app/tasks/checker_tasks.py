import asyncio
from celery import shared_task
from app.services.checker import run_all_price_checks
from app.db.session import engine  

async def _async_runner():
    try:
        await run_all_price_checks()
    finally:
        await engine.dispose()
        
@shared_task
def run_all_trackings_check():
    asyncio.run(_async_runner())