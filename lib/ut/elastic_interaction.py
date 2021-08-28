import requests
import json
from requests.auth import HTTPBasicAuth


class Elastic(object):

    def __init__(self):

        self.ELASTIC_SEARCH_URL = "https://c-c9qc3vfnqlo9av21d79a.rw.mdb.yandexcloud.net:9200/"
        self.LOGIN = "***"
        self.PASSWORD = "***"
        self.INDEX_NAME = "gpn_01"
        self.headers = {"Content-Type": "application/json"}

    def get_results(self, query):
        params = {
            "query": {
                "query_string": {
                    "query": query
                }
            }
        }
        # params = {
        #     'query': {
        #         'match': {
        #             'query': query
        #         }
        #     }
        # }
        resp = requests.get(url=self.ELASTIC_SEARCH_URL + "_search", data=json.dumps(params), verify="./lib/ut/root.crt",
                            auth=HTTPBasicAuth(self.LOGIN, self.PASSWORD), headers=self.headers)
        return resp.json()

    def insert_document(self, doc):
        resp = requests.post(url=self.ELASTIC_SEARCH_URL + self.INDEX_NAME + "/_doc", data=json.dumps(doc), verify="./lib/ut/root.crt",
                             auth=HTTPBasicAuth(self.LOGIN, self.PASSWORD), headers=self.headers)
        print(resp.text)

    def delete_index(self):
        resp = requests.delete(url=self.ELASTIC_SEARCH_URL + self.INDEX_NAME, verify="./lib/root.crt",
                               auth=HTTPBasicAuth(self.LOGIN, self.PASSWORD),
                               headers=self.headers)
        print(resp)

    def create_index(self):
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
        resp = requests.put(url=self.ELASTIC_SEARCH_URL + self.INDEX_NAME, verify="./root.crt", data=json.dumps(index),
                            auth=HTTPBasicAuth(self.LOGIN, self.PASSWORD),
                            headers=self.headers)
        print(resp)


# delete_index()
# create_index()
# if __name__ == '__main__':
#     elastic = Elastic()
#     print(elastic.get_results('Газ'))

# insert_document(doc)
