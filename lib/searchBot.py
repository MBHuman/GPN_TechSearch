import requests
from bs4 import BeautifulSoup

'''

Источники информации:

    * Yandex.maps
    * Ринц
    * 
'''

class SearchEngine(object):

    def __init__(self):
        self.main_part='https://yandex.ru/search/?text=&ncrnd=35822'
        self.search_parts=[]
        self.search_conditions=[]

    def search(self, word=''):
        
        search_part = self.main_part+word
        req = requests.post(search_part)

        soup = BeautifulSoup(req.text, 'html.parser')
        
    def split_parts(self, searches):
        returns = []
        if(searches == None):
            return returns
        
        splitted = searches.split('OR')

        for i in range(len(splitted)):
            splitted[i] = splitted[i].strip()

            temp = splitted[i].split('AND')
            to_returns = []
            for j in temp:
                to_returns.append(j.strip())

            returns.append(to_returns)

        return returns

    def split_to_search_blocks(self, search_string):
        search_string = search_string.strip()
        splited_block = search_string.split('|')

        block1_all = None
        block2_reduce = None

        if(len(splited_block) == 1):
            block1_all = splited_block[0]
        elif(len(splited_block) == 2):
            block1_all = splited_block[0]
            block2_reduce = splited_block[1]
        else:
            raise Exception('Ошибка в запросе')
        
        self.search_parts = self.split_parts(block1_all)
        self.search_conditions = self.split_parts(block2_reduce)

    def is_correct(self, search):
        if(search.count('|') > 1):
            return False
        return True

    def corrector_basic(self, search):
        ''' Правила синтаксиса поиска

            [Блок 1 - общий запрос] - Область поиска в широком виде
            [Блок 2 - ограничение] - Исключение нерелевантных результатов

            Операторы поиска:

            Оператор усечения `+`
            Оператор ИЛИ `OR` (Для Яндекса можно поставить | в поиске)
            Оператор И `AND` (Для Яндекса можно поставить & в поиске)
            Оператор указания, что может находиться n или меньше слов в любом порядке `nD`
            Оператор указания, что может находиться n или меньше слов в строгом порядке `nW`

        '''
        if(not self.is_correct(search)):
            raise Exception('Не корректный запрос')

        self.split_to_search_blocks(search)



if __name__ == '__main__':
    engine = SearchEngine()
    word = 'name для работы с 25W OR fire OR кобальт AND новый 12D уренгой AND <<раскопки>> | Раскопки новые |'
    engine.corrector_basic(word)
    print(engine.search_parts)
    print(engine.search_conditions)
