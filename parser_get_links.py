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
    print(fact_element)
    # Проверяем наличие элемента
    if fact_element:
        # Извлекаем ссылки из элемента
        for link in fact_element.find_all('a', href=True):
            link_href = link['href']
            links.append(link_href)

    return links

# Основная часть программы
if __name__ == '__main__':
    url = 'https://auto.drom.ru/region38/toyota/probox/year-2004/'
    html = get_html(url)
    fact_links = parse_page(html)

    # Выводим полученные ссылки на факты продаж
    print('Ссылки на факты продаж:')
    for link in fact_links:
        print(link)
