from bs4 import BeautifulSoup
import json
from collections import Counter

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_file = file.read()

    star = BeautifulSoup(xml_file, "xml").star
    item = {}
    for el in star:
        if el.name is None:
            continue
        item[el.name] = el.get_text().strip()

    item['radius'] = int(item['radius'])

    return item

data = []
for i in range(1, 108):
    data.append(handle_file(f"data/3/{i}.xml"))

with open("third_task_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

sorted_by_radius = sorted(data, key=lambda x: x['radius'], reverse=True)
with open("third_task_sorted_by_radius.json", "w", encoding="utf-8") as file:
    json.dump(sorted_by_radius, file, ensure_ascii=False, indent=4)

filtered_by_constellation = [star for star in data if star.get('constellation') == 'Весы']
with open("third_task_filtered_by_constellation.json", "w", encoding="utf-8") as file:
    json.dump(filtered_by_constellation, file, ensure_ascii=False, indent=4)

radii = [star['radius'] for star in data]
radius_stats = {
    "sum": sum(radii),
    "min": min(radii),
    "max": max(radii),
    "average": sum(radii) / len(radii),
}

constellation_frequency = Counter(star['constellation'] for star in data if 'constellation' in star)

print("Характеристики радиуса:")
print(f"Сумма: {radius_stats['sum']}")
print(f"Минимум: {radius_stats['min']}")
print(f"Максимум: {radius_stats['max']}")
print(f"Среднее: {radius_stats['average']:.2f}")

print("Частота созвездий':")
for constellation, count in constellation_frequency.items():
    print(f"{constellation}: {count}")
