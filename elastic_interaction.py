import requests
import json


ELASTIC_SEARCH_URL = "https://c-c9qc3vfnqlo9av21d79a.rw.mdb.yandexcloud.net:9200/"
LOGIN = "***"
PASSWORD = "****"
INDEX_NAME = "gpn_01"
from requests.auth import HTTPBasicAuth

headers = {"Content-Type": "application/json"}


def get_results(query):
    params = {"query": {
        "query_string": {
            "query": query
        }
    }
    }
    resp = requests.get(url=ELASTIC_SEARCH_URL + "_search", data=json.dumps(params), verify="./root.crt",
                        auth=HTTPBasicAuth(LOGIN, PASSWORD), headers=headers)
    return json.loads(resp.text)


def insert_document(doc):
    resp = requests.post(url=ELASTIC_SEARCH_URL + INDEX_NAME + "/_doc", data=json.dumps(doc), verify="./root.crt",
                         auth=HTTPBasicAuth(LOGIN, PASSWORD), headers=headers)
    print(resp.text)


def delete_index():
    resp = requests.delete(url=ELASTIC_SEARCH_URL + INDEX_NAME, verify="./root.crt",
                           auth=HTTPBasicAuth(LOGIN, PASSWORD),
                           headers=headers)
    print(resp)


def create_index():
    index = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "address": {"type": "text"},
                "emails": {"type": "text"},
                "phones": {"type": "text"},
                "url": {"type": "text"},
                "description": {"type": "text"},
                "additional_info": {"type": "text"},
                "categories": {"type": "text"},
                "update_date_time": {"type": "date"}
            }
        }
    }
    resp = requests.put(url=ELASTIC_SEARCH_URL + INDEX_NAME, verify="./root.crt", data=json.dumps(index),
                        auth=HTTPBasicAuth(LOGIN, PASSWORD),
                        headers=headers)
    print(resp)


# delete_index()
# create_index()
get_results("Газпром")
doc = {
    "name": "Газпром",
    "address": "Лахтинский проспект, д. 2, корп. 3, стр. 1, Санкт-Петербург, 197229",
    "emails": "gazprom@gazprom.ru",
    "phones": "+7 812 413-74-44",
    "url": "https://ru.wikipedia.org/wiki/Газпром",
    "description": "российская транснациональная энергетическая компания, более 50 % акций которой принадлежит государству. Является холдинговой компанией Группы «Газпром». Непосредственно ПАО «Газпром» осуществляет только продажу природного газа и сдаёт в аренду свою газотранспортную систему. Основные направления деятельности — геологоразведка, добыча, транспортировка, хранение, переработка и реализация газа, газового конденсата и нефти, реализация газа в качестве моторного топлива, а также производство и сбыт тепло- и электроэнергии[5]. «Газпром» является владельцем значительной части акций дочерней компании отрасли услуг электросвязи Газпром космические системы.",
    "additional_info": "",
    "categories": "Холдинг, Газ, Нефть, Интернет",
}
# insert_document(doc)
