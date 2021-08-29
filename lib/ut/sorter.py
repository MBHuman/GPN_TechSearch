import pandas as pd
from collections import defaultdict
from gensim import corpora, models, similarities
from nltk.corpus import stopwords as nltk_stopwords
from pymystem3 import Mystem
import re

from sklearn.feature_extraction.text import TfidfVectorizer  # ,CountVectorizer
from sklearn.preprocessing import StandardScaler
from scipy.stats import logistic
from scipy.spatial.distance import cosine as dist

from nltk.stem.snowball import SnowballStemmer



# input_data = pd.read_csv('input.csv')
#
# input_data = input_data[['name', 'description', 'category']]
#
# input_data['description'] = input_data['description'].apply(lambda x: x.split(',')[-2])
# input_data['city'] = input_data['description']
# input_data = input_data.drop('description', axis=1)
#
# input_data = input_data.rename(columns={'name': 'name_company',
#                                         'category': 'categories',
#                                         'description': 'city'})
#
# #####################
# ## Структура данных ##
# #####################
#
# ####################################################################################
# ####################################################################################
# '''
# data_structure = {'name_company': object,
#                   'categories':object,
#                   'city':object
#                  }
#
# Требования к данным:
# 1. 'name_company' - название компании
#     - может быть и пустой строкой вида '' (заполнить)
#     - имеет ограничение по количеству символов ~30
# 2. 'categories' - отрасль компании
#     - НЕ МОЖЕТ быть пустой строкой (иначе компания вообще не будет индексироваться и попадать в выдачу)
#     - имеет ограничение по количеству символов ~200
# 3. 'city' - город в котором зарегистрирована компания
#     - имеет ограничение по количеству символов ~30
#     - НЕ МОЖЕТ быть пустой строкой
#
#
# '''
#
#
#
#
# ########################################################################
# ########################################################################
#
# ###########################
# ##  Здесь проверки качества ##
# ##########################
#
#
#
#
# data = checking_data(input_data)
#
# ########################################################################
# ########################################################################
#
# comp_names = data['name_company'].tolist()
# documents = data['categories'].tolist()
# city = data['city'].tolist()
#
# TARGET = "металлопрокат, цветные металлы самара "
#
# data['categories'] = documents
#
# stoplist = set(nltk_stopwords.words('russian'))
#
# regexp = r'[^а-яА-ЯeЁ0-9]'
#
# lemm_categories = lemm_list(data['categories'], regexp)
# TARGET = lemmatize(TARGET, regexp)
#
# stemm_target = stemmer(TARGET)
#
# dist_data = rait_by_distance(lemm_categories, TARGET)
#
# relevance_data = pd.DataFrame(data={'rait_cat': rait_categories(lemm_categories, TARGET),
#                                     # 'proxi_desc':dist_data['proxi_desc'],
#                                     'proxi_keys': dist_data['proxi_keys']
#                                     })
#
# relevance_data['word_in_name'] = is_query_in_title(comp_names, stemm_target).values()
# relevance_data['cities_matched'] = is_city_in_query(city, TARGET)
#
# # Вычисляем итоговый рейтинг компаний
# '''
# relevance_data['final_reit'] = (relevance_data.rait_cat * relevance_data.proxi_keys * ( 1 + (
#                              relevance_data.comm_weight + relevance_data.rait + relevance_data.proxi_desc +\
#                              relevance_data.have_email))) / (1 - relevance_data.word_in_name)
# '''
#
# relevance_data['final_reit'] = (relevance_data.rait_cat * relevance_data.proxi_keys / (1 - relevance_data.word_in_name))
#
# sorted_relevance_data = relevance_data.join(input_data['categories']).sort_values(['cities_matched', 'final_reit'],
#                                                                                   ascending=[False, False])
# # display(sorted_relevance_data)
#
# # if sorted_relevance_data.loc[sorted_relevance_data['cities_matched'] == 1]['cities_matched'].count() == 0:
# #    print('Извините, по указанному региона поиска результатов выдачи нет. Но вы можете посмотреть на компании из других регионов:')
# final_output = sorted_relevance_data.index.to_list()
# final_output

class Sorter(object):

    def __init__(self, TARGET):

        self.data_structure = {'name_company': object,
                          'categories': object,
                          'city': object
                          }
        stemm_target = self.stemmer(TARGET)

    def clean_text(self, expression, replacement, text):
        text_wo_re = re.sub(expression, replacement, text)
        return ' '.join(text_wo_re.split())

    def lemmatize(self, text, expression):
        m = Mystem()
        clear_text = self.clean_text(expression, ' ', text)
        lemm_text_list = m.lemmatize(clear_text)
        return self.clean_text(expression, ' ', " ".join(lemm_text_list))

    def checking_data(self, data):
        for col in data.columns:
            try:
                if self.data_structure[col] in [int, float]:
                    fill = 0
                elif self.data_structure[col] == object:
                    fill = ''
                data[col] = data[col].fillna(fill)
                try:
                    if not isinstance(data.loc[0, col], self.data_structure[col]):
                        data[col] = data[col].astype(self.data_structure[col])
                except:
                    print('Неверный выходной тип данных. Колонка {}. Ожидалось {}. Пришло {}'.format(col,
                                                                                                     self.data_structure[
                                                                                                         col],
                                                                                                     type(
                                                                                                         data.loc[
                                                                                                             0, col])))
            except:
                print('Проблема с типом входных данных. Неизвестный формат у {}'.format(col))
        return data

    def lemm_list(self, text, expression):
        lemm = []
        for text in data['categories']:
            lemm.append(self.lemmatize(text, expression=regexp))
        return lemm

    def stemmer(self, sentense):
        words = sentense.split(' ')
        snow_stemmer = SnowballStemmer(language='russian')
        stemm_sentense = []
        for word in words:
            stemm_sentense.append(snow_stemmer.stem(word))
        return ' '.join(stemm_sentense)

    def is_query_in_title(self, comp_names, TARGET):
        companies = []
        for i in comp_names:
            companies.append(i.lower())
        num_inter = {}
        counter = 0
        for i in comp_names:
            num_inter[str(counter)] = 0
            for j in TARGET.split():
                if j in i.lower():
                    num_inter[str(counter)] += 1
            num_inter[str(counter)] = num_inter[str(counter)] / (len(i.split()) + len(self.stemm_target.split()))
            counter += 1
        return num_inter

    def is_city_in_query(self, cities_list, TARGET):
        TARGET = TARGET.split()
        cities = []
        for i in cities_list:
            i = i.strip().lower()
            if i in TARGET:
                cities.append(1)
            else:
                cities.append(0)
        return cities

    def rait_categories(self, lemm_categories, TARGET):
        global stoplist, regexp

        texts = [
            [word for word in document.lower().split() if word not in stoplist]
            for document in lemm_categories
        ]

        # remove words that appear only once
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        lemm_categories = [
            [token for token in text if frequency[token] >= 1]
            for text in texts
        ]

        dictionary = corpora.Dictionary(lemm_categories)
        corpus = [dictionary.doc2bow(text) for text in lemm_categories]

        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

        vec_bow = dictionary.doc2bow(TARGET.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space

        index = similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]

        ### не уверен в работе этого ###
        index.save('/tmp/deerwester.index')
        index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

        sims = enumerate(sims)
        doc_rait = []
        doc_pos = []
        for doc_position, doc_score in sims:
            doc_rait.append(doc_score)
            doc_pos.append(doc_position)

        data = pd.Series(doc_rait)
        return data

    def rait_by_distance(self, lemm_categories, TARGET):
        global stoplist, regexp
        # Инициализируем векторайзер
        count_tf_idf = TfidfVectorizer(stop_words=stoplist)
        # Векторизуем корпус текстов "категории"

        tf_idf_key = count_tf_idf.fit_transform(lemm_categories)

        # Векторизуем таргет
        tf_idf_target = count_tf_idf.transform([TARGET])

        # Создаем новый датафрейм, куда помещаем векторизованные сущности
        text = pd.DataFrame()
        text['vect_keys'] = list(tf_idf_key.toarray())

        # Костыль для заполнения столбца таргета вектором
        target_list = list(tf_idf_target.toarray())
        text['target'] = 0
        text['target'] = text['target'].apply(lambda x: target_list)

        # Теперь вычисляем косинусное расстояние между текстами
        text['dist_keys'] = text.apply(lambda x: dist(x['vect_keys'], x['target']), axis=1)

        # Переводим косинусное расстояние в меру близости
        text['proxi_keys'] = 1 - text['dist_keys']
        text = text.fillna(0)
        return text[['proxi_keys']]  # text[['proxi_desc', 'proxi_keys']]



