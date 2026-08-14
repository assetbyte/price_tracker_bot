from bs4 import BeautifulSoup
with open("ktzh_direct_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
elements = soup.select("table.table tr")

print(f"Found{len(elements)}")

for idx, elem in enumerate(elements, 1):
    text = " | ".join([line.strip() for line in elem.get_text().split("\n") if line.strip()])
    if text:
        print(f"[{idx}] {text[:1000]}...") 