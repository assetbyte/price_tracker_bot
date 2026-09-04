from datetime import datetime, timedelta, timezone
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_popular_stations() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Almaty"),
                KeyboardButton(text="Astana"),
                KeyboardButton(text="Shymkent"),
            ],
            [
                KeyboardButton(text="Karaganda"),
                KeyboardButton(text="Aktobe"),
                KeyboardButton(text="Pavlodar"),
            ],
            [
                KeyboardButton(text="Atyrau"),
                KeyboardButton(text="Taraz"),
                KeyboardButton(text="Ust-Kamenogorsk"),
            ],
            [
                KeyboardButton(text="/cancel")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
def get_quick_date() -> ReplyKeyboardMarkup:
    kz_timezone = timezone(timedelta(hours=5))
    today = datetime.now(kz_timezone).date()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=today.strftime("%Y-%m-%d")),
                KeyboardButton(text=tomorrow.strftime("%Y-%m-%d")),
                KeyboardButton(text=day_after_tomorrow.strftime("%Y-%m-%d")),
            ],
            [
                KeyboardButton(text="/cancel")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
def get_car_types() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Плацкарт"),
                KeyboardButton(text="Купе"),
                KeyboardButton(text="Люкс"),
            ],
            [
                KeyboardButton(text="Any"),
            ],
            [
                KeyboardButton(text="/cancel")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )