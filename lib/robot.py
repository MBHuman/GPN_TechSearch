import json
import requests
# from selenium import webdriver
#
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

    def __init__(self, yandex_api_key=None):
        self.connection_data = ConnectionStructure(host='localhost',
                                                   database='std_1455_gpn',
                                                   user='std_1455_gpn',
                                                   password='12345678')

        self.yandex_api_key = yandex_api_key
        self.search_keys = self.get_keys()

    def join_strings(self, string):
        if(not isinstance(string, list) and not isinstance(string, str)):
            raise Exception('Not string')
        if(isinstance(string, list)):
            return ', '.join(string)
        return string

    def get_keys(self):
        with open('./lib/search_keys.json') as file:
            data = json.loads(file.read())
        if not data:
            raise Exception('Не заполнен search_keys.json. Сделайте set_keys()')
        return data

    def set_keys(self):

        open('search_keys.json', 'w').close()

        search = {
            'types': [
                {
                    'type': 'Отрасль',
                    'id_type': 1,
                    'attributes': [
                        {
                            'name': 'Энергетика'
                        },
                        {
                            'name': 'Добыча полезных ископаемых'
                        },
                        {
                            'name': 'Строительство'
                        },
                        {
                            'name': 'Металлургия'
                        },
                        {
                            'name': 'Химическая и нефтехимическая промышленность'
                        },
                        {
                            'name': 'Машиностроение'
                        },
                        {
                            'name': 'Металлообработка'
                        },
                        {
                            'name': 'Производство строительных материалов'
                        }
                    ]
                },
                {
                    'type': 'Сфера применения',
                    'id_type': 2,
                    'attributes': [
                        {
                            'name': 'Геологоразведческие работы'
                        },
                        {
                            'name': 'Геология и разработка месторождений нефти и газа'
                        },
                        {
                            'name': 'Добыча нефти и газа'
                        },
                        {
                            'name': 'Нефтегазосервис (Upstream)'
                        },
                        {
                            'name': 'Транспорт и хранение нефти и газа (Midstream)'
                        },
                        {
                            'name': 'Энергоэффективность'
                        },
                        {
                            'name': 'Нефтегазопереработка'
                        },
                        {
                            'name': 'Нефтегазохимия'
                        },
                        {
                            'name': 'СПГ'
                        },
                        {
                            'name': 'сбыт (Downstream)'
                        }
                    ]
                },
                {
                    'type': ' Продукты',
                    'id_type': 3,
                    'attributes': [
                        {
                            'name': 'Конкретные технологии',
                            'additionally': [
                                {
                                    'name': 'Исследование скважин'
                                },
                                {
                                    'name': 'Методы увеличения нефтеотдачи'
                                },
                                {
                                    'name': 'Методы интенсификация добычи'
                                }
                            ]
                        },
                        {
                            'name': 'Оборудование и материалы',
                            'additionally': [
                                {
                                    'name': 'насосно-компрессорные трубы'
                                },
                                {
                                    'name': 'обсадные трубы'
                                },
                                {
                                    'name': 'ЭЦН'
                                },
                                {
                                    'name': 'жидкости ГРП'
                                },
                                {
                                    'name': 'проппант'
                                },
                                {
                                    'name': 'композитные материалы'
                                }

                            ]
                        }
                    ]
                }
            ]
        }
        with open('search_keys.json', 'w') as file:
            json.dump(search, file)

    def start_bot(self):
        self.get_info_yandex_maps()
        # while (True):


    def get_info_yandex_maps(self):
        '''
            Информация по API взята с этой страницы
            https://yandex.ru/dev/maps/geosearch/doc/concepts/about.html
        :return: None
        '''
        if not self.yandex_api_key:
            raise Exception('API ключ не предоставлен')

        search_query = f'https://search-maps.yandex.ru/v1/?text=Машиностроение&type=geo&lang=ru_RU&type=biz&apikey={self.yandex_api_key}'
        req = requests.get(search_query)

        self.json_data = req.json()

    def get_json_data_from_yandex(self):
        if not self.json_data:
            raise Exception('Сделайте запрос заддных через get_info_yandex_maps')
        return self.json_data

    def find_info_from_webpage(self):
        pass

    def make_webpage_graph(self):
        pass


    def search_web(self):
        pass