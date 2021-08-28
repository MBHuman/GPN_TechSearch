from robot import Robot
import json

def set_keys():

    open('search_keys.json', 'w').close()

    search = {
        'types': [
            {
                'type' : 'Отрасль',
                'id_type' : 1,
                'attributes': [
                    {
                        'name' : 'Энергетика'
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
    print(search)

if __name__ == '__main__':
    # bot = Robot(yandex_api_key='')
    # bot.get_info_yandex_maps()
    # data = bot.get_json_data_from_yandex()
    # with open('company_data.json', 'w') as file:
    #     json.dump(data, file)

    # data = None
    # with open('company_data.json') as file:
    #     data = json.loads(file.read())
    # names = data['features']
    # print(len(names))
    # for name in names:
    #     print(name['properties']['CompanyMetaData']['name'])

    # open('search_keys.json', 'w').close()
    set_keys()
