import requests
from bs4 import BeautifulSoup
import json

class CarScraper:
    def __init__(self, brand, model, year):
        if not isinstance(year, int):
            raise ValueError("Год должен быть целым числом.")
        self.brand = brand
        self.model = model
        self.year = year
        self.base_url = f'https://auto.drom.ru/region38/{brand}/{model}/year-{year}/'
        self.current_url = self.base_url

    def get_html(self, url):
        response = requests.get(url)
        return response.text

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        class_name = 'css-1nvf6xk eojktn00'
        fact_element = soup.find('div', class_=class_name)
        if fact_element:
            for link in fact_element.find_all('a', href=True):
                link_href = link['href']
                links.append(link_href)
        return links

    def extract_price_and_year(self, url):
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

    def scrape(self):
        html = self.get_html(self.current_url)
        links = self.parse_page(html)

        while len(links) < 5:
            last_segment = self.current_url.split('-')[-1]
            if last_segment[:4].isdigit():
                start_year = int(last_segment[:4])
                self.current_url = self.base_url.replace(f'year-{start_year}/',
                                                         f'?minyear={start_year - 1}&maxyear={start_year + 1}/')
                html = self.get_html(self.current_url)
                links = self.parse_page(html)

        car_data = {}

        for link in links:
            price, year = self.extract_price_and_year(link)
            if price is not None and year is not None:
                car_data[link] = {'price': price, 'year': year, 'link': link}

        return car_data

