import requests
from bs4 import BeautifulSoup

# Функция для получения HTML-кода страницы
def get_html(url):
    response = requests.get(url)
    return response.text

# Функция для парсинга страницы и извлечения ссылок на факты продаж
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    # Определите класс HTML, в котором нужно осуществить поиск ссылок
    class_name = 'css-1nvf6xk eojktn00'

    # Находим элемент с указанным классом
    fact_element = soup.find('div', class_=class_name)
    # Извлекаем ссылки из элементов и добавляем их в список
    for link in fact_element.find_all('a', href=True):
        link_href = link['href']
        links.append(link_href)

    return links

# Основная часть программы
if __name__ == '__main__':
    base_url = 'https://auto.drom.ru/region38/toyota/probox/year-2005/'
    links = []
    current_url = base_url

    if len(links) < 5:
        links = []
        start_year = int((current_url.split('-')[-1])[:4])
        current_url = base_url.replace(f'year-{start_year}/', f'?minyear={start_year - 1}&maxyear={start_year + 1}/')
        html = get_html(current_url)
        print('Ссылки на факты продаж:')
        fact_links = parse_page(html)
        for link in fact_links:
            print(link)
        # print(fact_links)
    else:
         # Выводим полученные ссылки на факты продаж
        print('Ссылки на факты продаж:')
        for link in links:
            print(link)