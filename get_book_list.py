import requests
import json
from bs4 import BeautifulSoup

def parse_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    class_names = {
        'Clasa a I-a': 1,
        'Clasa a II-a': 2,
        'Clasa a III-a': 3,
        'Clasa a IV-a': 4,
        'Clasa a V-a': 5,
        'Clasa a VI-a': 6,
        'Clasa a VII-a': 7,
        'Clasa a VIII-a': 8,
        'Clasa a IX-a': 9,
        'Clasa a X-a': 10,
        'Clasa a XI-a': 11,
        'Clasa a XII-a': 12,
        'Limba Engleza': 13,
        'Limba Franceza': 14
    }

    response = requests.get(url, headers=headers)
    data = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        book_classes = soup.find_all(class_='bookClass')
        for book_class in book_classes:
            class_name = book_class.find_previous('div').text.strip()
            class_name = class_names.get(class_name, class_name)

            links = book_class.find_all('a')
            for link in links:
                link_url = link.get('href')
                file_name = link.find('span').text

                if class_name not in data:
                    data[class_name] = [{'NAME': file_name, 'LINK': link_url}]
                else:
                    data[class_name].append({'NAME': file_name, 'LINK': link_url})

        return data

    else:
        print('Ошибка при получении страницы')
        return None
