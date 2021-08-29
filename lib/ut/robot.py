import json
import requests
from lib.ut.results import Result
from lib.ut.elastic_interaction import Elastic
import time
import random
import re
import networkx as nx
from threading import Thread
from selenium import webdriver

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

class RobotExtention(object):

    def __init__(self, page_object):
        self.page_object = page_object

    def set_random_time_sleep(self):
        time.sleep(random.gauss(2, 1))

    def is_yandex_search_page(self):
        if self.page_object.current_url.find('https://yandex.ru/search/') == -1:
            return False
        return True

    def is_yandex_capcha_page(self):
        if self.page_object.current_url.find('https://yandex.ru/showcaptcha') == -1:
            return False
        return True

    def close_yandex_capcha(self):
        if self.is_yandex_capcha_page():
            self.page_object.find_element_by_class_name('CheckboxCaptcha-Anchor').click()

    def get_next_page(self):
        if not self.is_yandex_page():
            raise Exception('Not yandex page')

        next_button = self.page_object.find_element_by_class_name('pager__item_kind_next')
        next_button.click()

    def get_serps_on_page(self):
        return self.page_object.find_elements_by_class_name('serp-item')




class Robot(object):

    def __init__(self, yandex_api_key=None):
        self.set_keys()

        self.yandex_api_key = yandex_api_key
        self.search_keys = self.get_keys()
        self.elastic = Elastic()
        self.patternDistance = re.compile(r"(?P<Distance> \s?[0-9])[d|w]", re.VERBOSE)
        self.plusSignReplace = re.compile(r"(?P<PlusSign> \S*)\+", re.VERBOSE)

    def is_valid_block(self, search):
        if search.find('[') == -1 and search.find(']') == -1:
            return (True, 0)

        if search.count('[') == 1 and search.count(']') == 1:
            if search[0] == '[' and search[-1] == ']':
                return (True, 1)

        if search.count('[') == 2 and search.count(']') == 2:
            if search[0] == '[' and search[-1] == ']':
                if search[search.find(']') + 1] == '[':
                    return (True, 2)

        return (False, 0)

    def transform_to_common(self, search):

        validation = self.is_valid_block(search)

        common = ''
        not_criteria = ''

        if validation[0]:
            if validation[1] == 0:
                common += search
            else:
                left = 0
                for char in search:
                    if char == '[':
                        left += 1
                    elif left <= 1 and char != ']':
                        common += char
                    elif left >= 1 and char != ']':
                        not_criteria += char
            return (common, not_criteria)
        return (common, not_criteria)


    def query_translator(self, common, not_criteria):
        """translate GPN to elasticsearch query.
            1. nD and nW to ~n . Но выдачу собственно надо будет смотреть по релевантности выдачи по этим параметрам
            2. Заменяем + на * в конце слова
        """
        result = ""
        com_temp = ""
        not_criteria_temp = ""
        if common:
            com_temp = self.patternDistance.sub("~\g<Distance>", common)
            com_temp = self.plusSignReplace.sub("\g<PlusSign>*", com_temp)
            result = com_temp

        if not_criteria:
            not_criteria_temp = self.patternDistance.sub("~\g<Distance>", not_criteria)
            not_criteria_temp = self.plusSignReplace.sub("\g<PlusSign>*", not_criteria_temp)
            result = com_temp + " AND NOT ( " + not_criteria_temp + ")"
        return result

    def get_results_from_elastic(self, search):
        commons = self.transform_to_common(search)
        search = self.query_translator(commons[0], commons[1])

        results = self.elastic.get_results(search)
        if 'status' in results:
            if results['status'] != 200:
                return 'Введите данные от Yandex Cloud в elastic_interaction.py'

        returns = []
        # print(results['hits']['hits'])
        for elem in results['hits']['hits']:
            res = Result()
            res.name = elem['_source']['name']
            res.link = elem['_source']['url']
            res.description = elem['_source']['description']
            res.phone = elem['_source']['phones']
            res.mail = elem['_source']['emails']
            res.category = elem['_source']['categories']
            res.address = elem['_source']['address']

            returns.append(res)

        return returns

    def join_strings(self, string):
        if(not isinstance(string, list) and not isinstance(string, str)):
            raise Exception('Not string')
        if(isinstance(string, list)):
            return ', '.join(string)
        return string

    def get_results_yandex_api(self, json_data):
        json_data = json_data['features']
        results = []
        for i in range(len(json_data)):
            cur_feature = json_data[i]['properties']

            temp = Result()
            temp.name = self.join_strings(cur_feature['name'])
            temp.mail = None
            temp.address = self.join_strings(cur_feature['CompanyMetaData']['address'])
            temp.description = cur_feature['description']

            categories = []
            for cat in cur_feature['CompanyMetaData']['Categories']:
                categories.append(cat['name'])

            temp.category = self.join_strings(categories)
            if 'url' in cur_feature['CompanyMetaData']:
                temp.link = cur_feature['CompanyMetaData']['url']

            phones = []
            if 'Phones' in cur_feature['CompanyMetaData']:
                for phone in cur_feature['CompanyMetaData']['Phones']:
                    phones.append(phone['formatted'])

            temp.phone = self.join_strings(phones)

            results.append(temp)
        return results

    def get_keys(self):
        with open('./lib/ut/jsons/search_keys.json') as file:
            data = json.loads(file.read())
        if not data:
            raise Exception('Не заполнен search_keys.json. Сделайте set_keys()')
        return data

    def set_keys(self):

        open('./lib/ut/jsons/search_keys.json', 'w').close()

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
        with open('./lib/ut/jsons/search_keys.json', 'w') as file:
            json.dump(search, file)

    def start_bot(self):
        self.get_info_yandex_maps()

        # while (True):


    def get_info_yandex_maps(self, search):
        '''
            Информация по API взята с этой страницы
            https://yandex.ru/dev/maps/geosearch/doc/concepts/about.html
        :return: None
        '''
        if not self.yandex_api_key:
            raise Exception('API ключ не предоставлен')

        search_query = f'https://search-maps.yandex.ru/v1/?text={search}&type=geo&lang=ru_RU&type=biz&results=500&apikey={self.yandex_api_key}'
        req = requests.get(search_query)

        return req.json()

    '''
    def get_json_data_from_yandex(self):
        if not self.json_data:
            raise Exception('Сделайте запрос заддных через get_info_yandex_maps')
        return self.json_data
    '''
    def add_to_elastic_res(self, result):

        for element in result:
            doc = {
                "name": element.name,
                "address": element.address,
                "emails": element.mail,
                "phones": element.phone,
                "url": element.link,
                "description": element.description,
                "additional_info": "",
                "categories": element.category
            }
            self.elastic.insert_document(doc)

    def load_data_into_elastic(self):

        with open('./lib/ut/jsons/search_keys.json') as file:
            main_themes = json.loads(file.read())

        for theme in main_themes['types']:
            block = theme['attributes']

            for elem in block:
                search_string = elem['name']

                if 'additionally' in elem:
                    advanced_search_string = search_string
                    for add in elem['additionally']:
                        advanced_search_string += '+'+add['name']

                        data = self.get_info_yandex_maps(advanced_search_string)
                        result = self.get_results_yandex_api(data)

                        self.add_to_elastic_res(result)

                else:
                    data = self.get_info_yandex_maps(search_string)
                    result = self.get_results_yandex_api(data)
                    self.add_to_elastic_res(result)

    def find_info_from_webpage(self):
        pass

    def make_webpage_graph(self):
        pass


    def search_web(self):
        pass

