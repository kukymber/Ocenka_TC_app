import requests
from bs4 import BeautifulSoup
import json

def get_html(url):
    response = requests.get(url)
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    class_name = 'css-1nvf6xk eojktn00'
    fact_element = soup.find('div', class_=class_name)
    if fact_element:
        for link in fact_element.find_all('a', href=True):
            link_href = link['href']
            links.append(link_href)
    return links

def extract_price_and_year(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при обращении к URL {url}, статус ответа: {response.status_code}")
            return None, None
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_element = soup.find('meta', attrs={'name': 'candy.config'})
        if meta_element is not None and 'content' in meta_element.attrs:
            content = meta_element['content']
            content_dict = json.loads(content)

            year = content_dict.get('cf', {}).get('y', None)
            price = content_dict.get('cf', {}).get('p', None)
        else:
            year = None
            price = None
        return price, year
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к URL {url}: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")
        return None, None

if __name__ == '__main__':
    base_url = 'https://auto.drom.ru/region38/toyota/probox/year-2004/'
    current_url = base_url
    html = get_html(current_url)
    links = parse_page(html)

    while len(links) < 5:
        start_year = int((current_url.split('-')[-1])[:4])
        current_url = base_url.replace(f'year-{start_year}/', f'?minyear={start_year - 1}&maxyear={start_year + 1}/')
        html = get_html(current_url)
        links = parse_page(html)

    car_data = {}

    for link in links:
        price, year = extract_price_and_year(link)
        if price is not None and year is not None:
            car_data[link] = {'price': price, 'year': year}

    for link, data in car_data.items():
        print(f"Ссылка: {link}\nЦена: {data['price']}₽\nГод выпуска: {data['year']}\n")
