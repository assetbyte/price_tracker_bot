import asyncio
from celery import shared_task
from app.services.checker import run_all_price_checks, run_cleanup_archive_trackings
from app.db.session import engine  
from sqlalchemy import select, update
from app.db.base import Tracking
from app.db.session import AsyncSessionLocal
from datetime import date

async def _async_runner(coro):
    try:
        return await coro
    finally:
        await engine.dispose()
        
@shared_task
def run_all_trackings_check():
    asyncio.run(_async_runner(run_all_price_checks()))
    
@shared_task
def run_cleanup_archive_active_trackings():
    cnt = asyncio.run(_async_runner(run_cleanup_archive_trackings()))
    return f"Number of archived tracking for today: {cnt}, ID: {run_cleanup_archive_active_trackings.request.id}"
    
    

    
    
    