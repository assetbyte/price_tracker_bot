import json
from bs4 import BeautifulSoup



def clean_int(value):
    result = ""
    for char in value:
        if char.isdigit():
            result+= char
            
    return int(result) if result else 0

def parse_html_to_json(html_content=None, output_json_path="ktzh_trains.json"):
    if html_content is None:
        with open("ktzh_direct_result.html", "r", encoding="utf-8") as f:
            html_content= f.read()


    soup = BeautifulSoup(html_content, "html.parser")
    
    early_return = soup.select(".ui.warning.message")
    if early_return:
        print("На выбранные даты еще нет билетов!")
        return {
            "total_records": 0,
            "tickets": []
        }
    
    
    rows = soup.select(".result-card__details table tbody tr")
    

    trains_data = []
    current_train = None

    for row in rows:
        row_car_type =  row.select_one(".result-card__details-table-car-type")
        row_free_seats = row.select_one(".result-card__details-table-seats-count")
        row_price = row.select_one(".result-card__details-table-cost")
        
        if row_car_type and row_free_seats and row_price:
            car_type_text = row_car_type.text.strip()
            free_seats_text = (row_free_seats.text.strip())
            price_text = (row_price.text.strip())

        # структура строки: [Вагон, Количество мест, Цена]
        # ["Купе", "15", "14 513 ₸"]
            car_info = {
                "car_type":     car_type_text,
                "free_seats": clean_int(free_seats_text),
                "price": clean_int(price_text)
            }

            trains_data.append(car_info)

    result = {
        "total_records": len(trains_data),
        "tickets": trains_data
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    return result

if __name__ == "__main__":
    data = parse_html_to_json()
    print(json.dumps(data, ensure_ascii=False, indent=2))