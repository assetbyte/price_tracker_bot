import json
from bs4 import BeautifulSoup

def parse_html_to_json(html_file_path="ktzh_direct_result.html", output_json_path="ktzh_trains.json"):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
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
                "free_seats": free_seats,
                "price": price
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