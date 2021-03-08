import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pymongo import MongoClient


"""
Выгружаем названия товаров, стоимость и ссылки на страницы товаров с сайта utkonos категории "Сладости, чай и кофе", сохраняем данные в БД MongoDB
"""

class UtkonosParse:

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client['utkonos_mining']
        self.collection = self.db.utkonos_collection

    def _get_response(self):
        #TODO : написать обработку ошибки
        return requests.get(url)

    def _get_soup(self):
        response = self._get_response()
        return BeautifulSoup(response.text, 'lxml')

    def _get_total_pages(self):
        """
        Находим количество страниц
        """
        return int(self._get_soup().findAll('li', {'class': 'pagination_item'})[-1].text)


    def parse(self):
        """
        Находим названия продуктов, цены и ссылки на страницы продуктов,
        добавляем полученные данные в БД
        """

        for page in range(1, self._get_total_pages() + 1):
            next_url = f"{url}page/{page}"
            response = requests.get(next_url)
            soup = BeautifulSoup(response.text, 'lxml')
            catalog = soup.findAll('div', attrs={'class': "product-card_middle-content"})

            for i in range(len(catalog)):
                catalog[i].find('a', attrs={'class': "utk-product-card-name"}).get('href')

                data = {'name': lambda a: catalog[i].find('span', attrs={'class': "d-sm-none"}).text,
                        'price': lambda a: float(catalog[i].find('span', attrs={'class': "product-price"}).text.replace(u'\xa0', '').replace(u'₽', '').replace(' ', '').replace(',', '.')),
                        'url': lambda a: urljoin(url, catalog[0].find('a', attrs={'class': "utk-product-card-name"}).get('href'))
                        }

                data_new = dict()
                for key, funk in data.items():
                    data_new[key] = funk(data_new)
                self.collection.insert_one(data_new)


if __name__ == "__main__":
    url = "https://www.utkonos.ru/cat/5274/"
    db_client = MongoClient('localhost', 27017)
    parser = UtkonosParse(url, db_client)
    parser.parse()
