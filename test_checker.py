import asyncio
from app.services.checker import run_all_price_checks

async def main():
    await run_all_price_checks()
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())