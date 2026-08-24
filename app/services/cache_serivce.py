import json
from typing import Any, Dict, Optional

from app.db.redis import redis_client
from scrapers.ktzh_client import get_ktzh_trains


CACHE_EXPIRE_SECONDS = 900 #15 minutes


async def get_cache_ktzh_trains(
    departure_code: str,
    arrival_code: str,
    departure_date: str,
) -> Optional[Dict[str, Any]]:
    
    cache_key = f"ktzh_schedule:{departure_code}:{arrival_code}:{departure_date}"
    
    try:
        cached_data = await redis_client.get(cache_key)
        if cached_data:
            print(f"Cache exists: {cache_key}")
            return json.loads(cached_data)
        
    except Exception as e:
        print(f"Error: {e}")
        
        
    print(f"CACHE MISS: ({cache_key})")
    parsed_data = await get_ktzh_trains(
        departure_code=departure_code,
        arrival_code=arrival_code,
        departure_date=departure_date
    )

    if not parsed_data:
        return None
    try:
        await redis_client.set(
            name=cache_key,
            value=json.dumps(parsed_data, ensure_ascii=False),
            expire=CACHE_EXPIRE_SECONDS
        )
    except Exception as e:
        print(f"Error {e}")

    return parsed_data

