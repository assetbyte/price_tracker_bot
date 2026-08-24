import os
from dotenv import load_dotenv
from redis.asyncio import Redis
load_dotenv()

REDIS_CACHE_URL = os.getenv("REDIS_CACHE_URL", "redis://localhost:6379/1")
redis_client = Redis.from_url(REDIS_CACHE_URL, decode_responses=True)