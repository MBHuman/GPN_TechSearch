from flask import Flask, render_template, request, send_file
import pickle
from lib.ut.robot import Robot


app = Flask(__name__)

results = []

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None

    if request.method == 'POST':
        search_field = request.form.get('search_field')

    # Get data from search_engine



    return( render_template('index.html'))

@app.route('/search', methods=['GET','POST'])
def search():
    robot = Robot()

    error, words = None, request.args.get('search_field')

    results = robot.get_results_from_elastic(words)
    # print(results)
    if(len(results) == 0):
        error = "По вашему запросу ничего не найдено"
    elif isinstance(results, str):
        error = results
        results = []
    robot.get_csv(results)
    return( render_template('results.html', words=words, error=error, results=results))

# @app.route('/download', methods=['POST', 'GET'])
# def download():
#     return send_file('static/first.csv', as_attachment=True)

@app.route('/info')
def info():
    return( render_template('info.html'))

if __name__ == '__main__':
    app.run()
