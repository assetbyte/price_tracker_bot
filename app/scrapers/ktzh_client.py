import asyncio
from bs4 import BeautifulSoup
import httpx
from ktzh_parser import parse_html_to_json

async def get_ktzh_trains(
    departure_code="2708001", 
    arrival_code="2700000", 
    departure_date="20-08-2026, чтв"
):
    url = "https://bilet.railways.kz/sale/default/route/search"
    
    params = {
        "route_search_form[departureStation]": departure_code,
        "route_search_form[arrivalStation]": arrival_code,
        "route_search_form[forwardDepartureDate]": departure_date,
        "route_search_form[backwardDepartureDate]": "",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36", 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://bilet.railways.kz/",
        "Accept-Language": "ru-KZ,ru;q=0.9,kk-KZ;q=0.8,kk;q=0.7",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }
    
    print("Sending request...")
    data = None
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=40) as client:
        try: 
            response = await client.get(url, params=params)
            
            response.raise_for_status() 
            
            print("Success:", response.status_code)
            
        
            data = parse_html_to_json(response.text)
        
        except Exception as e:
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {repr(e)}")
            
    return data

if __name__ == "__main__":
    asyncio.run(get_ktzh_trains())
    
    
    
    
  


