from datetime import datetime, timedelta, timezone
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_popular_stations(station_names: list[str]) -> ReplyKeyboardMarkup:
    keyboard_buttons = []
    row = []
    for name in station_names:
        row.append(KeyboardButton(text=name))
        if len(row) == 3:
            keyboard_buttons.append(row)
            row = []
    if row: 
        keyboard_buttons.append(row)
    keyboard_buttons.append([KeyboardButton(text="/cancel")])
    
    return ReplyKeyboardMarkup(
      keyboard=keyboard_buttons,
      resize_keyboard=True,
      one_time_keyboard=True,
  )
    
    
def get_quick_date() -> ReplyKeyboardMarkup:
    kz_timezone = timezone(timedelta(hours=5))
    today = datetime.now(kz_timezone).date()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=today.strftime("%d-%m-%Y")),
                KeyboardButton(text=tomorrow.strftime("%d-%m-%Y")),
                KeyboardButton(text=day_after_tomorrow.strftime("%d-%m-%Y")),
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
                KeyboardButton(text="/cancel")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )