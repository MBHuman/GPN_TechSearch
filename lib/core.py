from lib.ut.robot import Robot

class StringConverter(object):

    def __init__(self, search=''):
        self.search_parts=[]
        self.search_conditions=[]

        self.split_to_search_blocks(search)


    def split_parts(self, searches):
        returns = []
        if (searches == None):
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

        if (len(splited_block) == 1):
            block1_all = splited_block[0]
        elif (len(splited_block) == 2):
            block1_all = splited_block[0]
            block2_reduce = splited_block[1]
        else:
            raise Exception('Ошибка в запросе')

        self.search_parts = self.split_parts(block1_all)
        self.search_conditions = self.split_parts(block2_reduce)

    def is_correct(self, search):
        if (search.count('|') > 1):
            return False
        return True

class SpeedSearcher(object):

    def __init__(self):
        pass

    def get_objects(self, search_string):
        '''
            Здесь мы анализируем данные в нашей базе данных и
            выдаем наиболее выгодный результат

        '''

        self.converted_string = StringConverter(search_string)
        self.robot = Robot()


    def analyse(self):
        pass
