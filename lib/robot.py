from selenium import webdriver
import requests, mysql.connector, json


class ConnectionStructure(object):

    def __init__(self,
                 host=None,
                 database=None,
                 user=None,
                 password=None):
        self.host = host
        self.database = database
        self.user = user
        self.password = password


class Robot(object):

    def __init__(self):
        self.connection_data = ConnectionStructure(host='localhost',
                                                   database='std_1455_gpn',
                                                   user='std_1455_gpn',
                                                   password='12345678')

        self.yandex_api_key = '<API KEY>'
        self.lib_with_words = []

    def find_info_from_maps_yandex_maps(self):
        '''
            Информация по API взята с этой страницы
            https://yandex.ru/dev/maps/geosearch/doc/concepts/about.html
        :return: None
        '''
        search_query = f'https://search-maps.yandex.ru/v1/?text=Свободный, ул. Амурская, дом 18&type=geo&lang=ru_RU&apikey={self.yandex_api_key}'
        req = requests.get(search_query)

        self.json_data = req.json()


    def find_info_from_webpage(self):
        pass

    def make_webpage_graph(self):
        pass


    def search_web(self):

        pass