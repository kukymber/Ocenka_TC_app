import requests
from bs4 import BeautifulSoup
import re

def extract_price(url):
    try:
        response = requests.get(url)
        # Проверяем статус ответа
        if response.status_code != 200:
            print(f"Ошибка при обращении к URL {url}, статус ответа: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('div', class_='css-eazmxc e162wx9x0')
        if price_element is not None:
            price_text = price_element.text.strip()
            # Используйте регулярное выражение, чтобы извлечь числовое значение цены
            price = re.sub(r'\D', '', price_text)
            return int(price)  # Преобразовываем цену в числовой формат
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к URL {url}: {e}")
        return None

# Пример получения цены из ссылки
url = 'https://irkutsk.drom.ru/toyota/probox/50251096.html'
price = extract_price(url)
if price is not None:
    print('Цена авто:', price, '₽')
else:
    print('Не удалось получить цену авто с указанного URL')
