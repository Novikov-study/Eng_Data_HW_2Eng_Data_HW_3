import os
from bs4 import BeautifulSoup
import json
from collections import Counter
import statistics

def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return BeautifulSoup(file.read(), 'html.parser')

def parse_manga_file(file_path):
    soup = load_html(file_path)
    articles = soup.find_all('article')
    data = []
    for article in articles:
        name_en = article.find('span', class_='name-en')
        name_ru = article.find('span', class_='name-ru')
        year = article.find('span', class_='misc')
        if year and len(year.find_all('span')) > 1:
            year = year.find_all('span')[1].text.strip()
        else:
            year = None
        url = article.find('a', class_='cover')
        image_url = article.find('img')

        data.append({
            'name_en': name_en.text.strip() if name_en else "N/A",
            'name_ru': name_ru.text.strip() if name_ru else "N/A",
            'year': int(year) if year and year.isdigit() else None,
            'url': url['href'] if url else "N/A",
            'image_url': image_url['src'] if image_url else "N/A"
        })
    return data

def parse_html_folder(folder_path):
    data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(folder_path, file_name)
            soup = load_html(file_path)
            info = soup.find('div', class_='b-entry-info')
            if info:
                entry = {}
                for line in info.find_all('div', class_='line'):
                    key = line.find('div', class_='key')
                    value = line.find('div', class_='value')
                    if key and value:
                        key_text = key.text.strip()
                        value_text = [link.text.strip() for link in value.find_all('a')] if value.find_all('a') else value.text.strip()
                        entry[key_text] = value_text
                data[file_name] = entry
    return data

def process_manga_data(manga_data):
    sorted_data = sorted(manga_data, key=lambda x: x['year'] if x['year'] else float('inf'))
    filtered_data = [x for x in manga_data if x['year'] and x['year'] > 2000]
    years = [x['year'] for x in manga_data if x['year']]
    stats = {
        'min': min(years) if years else None,
        'max': max(years) if years else None,
        'mean': statistics.mean(years) if years else None,
        'median': statistics.median(years) if years else None
    }
    frequencies = Counter(x['name_ru'] for x in manga_data if x['name_ru'] != "N/A")
    return {
        'sorted': sorted_data,
        'filtered': filtered_data,
        'stats': stats,
        'frequencies': frequencies
    }

def process_html_data(html_data):
    sorted_data = dict(sorted(html_data.items()))
    filtered_data = {k: v for k, v in html_data.items() if 'Жанры' in v}
    genres = [genre for v in html_data.values() if 'Жанры' in v for genre in v['Жанры']]
    genre_freq = Counter(genres)
    return {
        'sorted': sorted_data,
        'filtered': filtered_data,
        'genre_frequencies': genre_freq
    }

def main():
    manga_file = 'Манга.html'
    html_folder = 'html'
    manga_output = 'manga_operations.json'
    html_output = 'html_operations.json'

    if os.path.exists(manga_file):
        manga_data = parse_manga_file(manga_file)
        manga_result = process_manga_data(manga_data)
        with open(manga_output, 'w', encoding='utf-8') as f:
            json.dump(manga_result, f, ensure_ascii=False, indent=4)

    if os.path.exists(html_folder):
        html_data = parse_html_folder(html_folder)
        html_result = process_html_data(html_data)
        with open(html_output, 'w', encoding='utf-8') as f:
            json.dump(html_result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
