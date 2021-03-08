from bs4 import BeautifulSoup
import requests
"""
Получаем котировку курса валюты HKD по отношению к RUB с сайта ЦБ РФ
"""
class ParcerCbr:
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'

    def _get_page(self):
        if requests.get(self.url).status_code == 200:
            return requests.get(self.url)
        else:
            print(f'Error {requests.get(self.url).status_code}')

    def _get_soup(self, arg):
        page = self._get_page()
        return BeautifulSoup(page.text, 'lxml')

    def _find_currency_value(self):
        soup = self._get_soup(self)
        valuteHKD = float(((soup.find('valute', {"id": "R01200"}).find('value').text).replace(',', '.')))
        nominalHKD = float(soup.find('valute', {"id": "R01200"}).find('nominal').text)
        rateHKD = valuteHKD/nominalHKD
        return rateHKD


p = ParcerCbr()

try:
    print(f'Rate HKD/RUB: {p._find_currency_value()}')
except AttributeError:
    print('AttributeError')




