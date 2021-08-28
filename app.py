from flask import Flask, render_template, request
from lib.ut.results import Result
from lib.robot import Robot
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None

    if request.method == 'POST':
        search_field = request.form.get('search_field')

    # Get data from search_engine



    return( render_template('index.html'))

@app.route('/search', methods=['GET'])
def search():
    error, words, results = None, request.args.get('search_field'), []
    robot = Robot()
    with open('./lib/train.json') as file:
        json_data = json.loads(file.read())
    # print(json_data)
    for i in range(20):
        cur_feature = json_data[i]['properties']

        temp = Result()
        temp.name = robot.join_strings(cur_feature['name'])
        temp.mail = None
        temp.address = robot.join_strings(cur_feature['CompanyMetaData']['address'])
        temp.description = cur_feature['description']

        categories = []
        for cat in cur_feature['CompanyMetaData']['Categories']:
            categories.append(cat['name'])

        temp.category = robot.join_strings(categories)
        if 'url' in cur_feature['CompanyMetaData']:
            temp.link = cur_feature['CompanyMetaData']['url']

        phones = []
        if 'Phones' in cur_feature['CompanyMetaData']:
            for phone in cur_feature['CompanyMetaData']['Phones']:
                phones.append(phone['formatted'])

        temp.phone = robot.join_strings(phones)

        results.append(temp)

    if(len(results) == 0):
        error = "По вашему запросу ничего не найдено"
    return( render_template('results.html', words=words, error=error, results=results))

@app.route('/info')
def info():
    return( render_template('info.html'))

if __name__ == '__main__':
    app.run()
