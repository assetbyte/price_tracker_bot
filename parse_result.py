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
    
    
    rows = soup.select("tr")

    trains_data = []
    current_train = None

    for row in rows:
        cols = [cell.text.strip() for cell in row.find_all(["td", "th"]) if cell.text.strip()]
        
        if not cols:
            continue

        if "Вагон" in cols[0]:
            continue

        # структура строки: [Вагон, Количество мест, Цена]
        # ["Купе", "15", "14 513 ₸"]
        if len(cols) >= 3:
            car_type = cols[0]
            free_seats = cols[1]
            price = cols[2]
            
            car_info = {
                "car_type": car_type,
                "free_seats": clean_int(free_seats),
                "price": clean_int(price)
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