from bs4 import BeautifulSoup
import json
from collections import Counter


def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    build = soup.find_all("div", attrs={'class': 'build-wrapper'})[0]
    item = {}
    item['city'] = build.find_all("span")[0].get_text().split(":")[1].strip()
    item['id'] = int(build.h1['id'])
    item['type'] = build.h1.get_text().split(":")[1].strip()
    address_temp = build.p.get_text().split("Улица:")[1].split("Индекс:")
    item['address'] = address_temp[0].strip()
    item['index'] = int(address_temp[1])
    item['floors'] = int(build.find_all("span", attrs={'class': 'floors'})[0].get_text().split(":")[1])
    item['year'] = int(build.find_all("span", attrs={'class': 'year'})[0].get_text().split("Построено в")[1])
    spans = build.find_all("span", attrs={'class': ''})
    item['parking'] = spans[1].get_text().split(":")[1].strip() == "да"
    item['rating'] = float(spans[2].get_text().split(":")[1])
    item['views'] = int(spans[3].get_text().split(":")[1])
    item['img'] = build.img['src']

    return item

data = []
for i in range(2, 91):
    result = handle_file(f"data/1/{i}.html")
    data.append(result)

with open("first_task_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

sorted_by_views = sorted(data, key=lambda x: x['views'], reverse=True)
with open("first_task_sorted_by_views.json", "w", encoding="utf-8") as file:
    json.dump(sorted_by_views, file, ensure_ascii=False, indent=4)
print("По просмотрам:")
for item in sorted_by_views:
    print(item)

city_to_filter = "Москва"
filtered_by_city = [item for item in data if item['city'] == city_to_filter]
print(f"Здания города {city_to_filter}:")
for item in filtered_by_city:
    print(item)

with open(f"first_task_filtered_by_city.json", "w", encoding="utf-8") as file:
    json.dump(filtered_by_city, file, ensure_ascii=False, indent=4)


views = [item['views'] for item in data]
views_stats = {
    "sum": sum(views),
    "min": min(views),
    "max": max(views),
    "average": sum(views) / len(views),
}

print("Характеристики просмотров:")
print(f"Sum: {views_stats['sum']}")
print(f"Min: {views_stats['min']}")
print(f"Max: {views_stats['max']}")
print(f"Average: {views_stats['average']:.2f}")

city_frequency = Counter(item['city'] for item in data)
print("\nЧастота городов:")
for city, count in city_frequency.items():
    print(f"{city}: {count}")

