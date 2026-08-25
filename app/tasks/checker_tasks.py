import asyncio
from celery import shared_task
from app.services.checker import run_all_price_checks


@shared_task
def run_all_trackings_check():
    asyncio.run(run_all_price_checks())