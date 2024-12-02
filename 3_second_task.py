from bs4 import BeautifulSoup
import re
import json
from collections import Counter


def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("div", attrs={'class': 'product-item'})
    items = []

    for product in products:
        item = {
            'id': int(product.a['data-id']),
            'link': product.find_all('a')[1]['href'],
            'img': product.img['src'],
            'title': product.span.get_text().strip(),
            'price': float(product.price.get_text().replace('₽', '').replace(' ', '').strip()),
            'bonus': int(re.sub(r'\D', '', product.strong.get_text()))
        }

        # Extracting properties
        properties = product.ul.find_all("li")
        for prop in properties:
            item[prop['type']] = prop.get_text().strip()

        items.append(item)

    return items


def process_files(file_paths):
    data = []
    for file_path in file_paths:
        data.extend(handle_file(file_path))

    with open("second_task_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    sorted_by_price = sorted(data, key=lambda x: x['price'], reverse=True)
    with open("second_task_sorted_by_price.json", "w", encoding="utf-8") as file:
        json.dump(sorted_by_price, file, ensure_ascii=False, indent=4)

    filtered_by_processor = [item for item in data if 'processor' in item]

    with open("second_task_filtered_by_processor.json", "w", encoding="utf-8") as file:
        json.dump(filtered_by_processor, file, ensure_ascii=False, indent=4)

    prices = [item['price'] for item in data]
    price_stats = {
        "sum": sum(prices),
        "min": min(prices),
        "max": max(prices),
        "average": sum(prices) / len(prices)
    }

    processor_frequency = Counter(item['processor'] for item in filtered_by_processor)

    print("\nСтатистические характеристики для цены:")
    print(f"Сумма: {price_stats['sum']:.2f}")
    print(f"Минимум: {price_stats['min']:.2f}")
    print(f"Максимум: {price_stats['max']:.2f}")
    print(f"Среднее: {price_stats['average']:.2f}")

    print("\nЧастота меток для 'processor':")
    for processor, count in processor_frequency.items():
        print(f"{processor}: {count}")

file_paths = [f"data/2/{i}.html" for i in range(1, 63)]
process_files(file_paths)
