import requests
from datetime import datetime

"""
Вывод максимальной утренней температуры за период +5 дней (вкл. текущий) 
с ресурса https://openweathermap.org/ и расчет средней утренней температуры за этот же период
"""


class ParserWheatherMoscow:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    DAYS = 5
    LATITUDE =55.7558
    LONGITUDE = 37.6173

    def _get_response(self):
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={self.LATITUDE}&lon={self.LONGITUDE}&units=metric&exclude=current,minutely,hourly,alerts&appid=63261a8061aa1061a6ca799ec7972557'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            print(f'Error {requests.get(url, headers=self.headers).status_code}')

    def _get_data_daily(self):
        """
        Получаем значения за промежуток от сегодняшнего до 5-го дня включительно
        """
        response = self._get_response()
        data = response.json().get('daily')[:int(self.DAYS)]
        return data

    def _get_data_morn(self):
        """
        Получаем значения dt, преобразуя его сразу в формат YYYY-MM-DD HH:MM:SS и значения morn по каждому dt, складываем полученные значения в словарь, а также вычисляем сумму всех значений morn
        """
        data = self._get_data_daily()
        data_morn_temp = dict()
        summa = 0
        for i in range(len(data)):
            date_and_time = datetime.utcfromtimestamp(int(data[i].get('dt'))).strftime('%Y-%m-%d %H:%M:%S')
            data_morn_temp[date_and_time] = data[i].get('temp').get('morn')
            summa += data_morn_temp[date_and_time]

        return data_morn_temp, summa

    def _find_max_temp(self):
        """
        Находим максимальное значение утренней температуры
        """
        max_morn_temp = max(self._get_data_morn()[0].values())
        dict_max_morn_temp = {k:v for k, v in self._get_data_morn()[0].items() if v == max_morn_temp}
        return dict_max_morn_temp




p = ParserWheatherMoscow()

"""
Оформляем вывод значений
"""
print(f'Location data latitude {p.LATITUDE} and longitude {p.LONGITUDE}')
print(f'Average morning temperature over the next 5 days (including today): {round(p._get_data_morn()[1]/p.DAYS, 2)}')

for key, value in p._find_max_temp().items():
    print(f'Maximum morning temperature: {value}, date: {key}')