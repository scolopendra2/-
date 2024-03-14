import pandas as pd

from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    data = pd.ExcelFile('_100 вопросов мастеру.xlsx')
    sheet_names = data.sheet_names
    return render_template('main.html', sheet_names=sheet_names)


@app.route('/sheet/<sheet_name>')
def sheet(sheet_name):
    viewed_questions = request.cookies.get(sheet_name).split(',')
    data = pd.read_excel('_100 вопросов мастеру.xlsx', sheet_name=sheet_name)
    data = data[~data['ФИО'].isin(viewed_questions)]
    count_question = len(data)
    random_question = data.sample(n=1)
    fio = random_question['ФИО'].values[0]
    position = random_question['Должность/курс'].values[0]
    place = random_question['Место работы/учёбы'].values[0]
    question = random_question['Вопрос'].values[0]
    resp = make_response(render_template('question.html', fio=fio, position=position,
                                         place=place, question=question, count_question=count_question))
    viewed_questions = ','.join(viewed_questions)
    viewed_questions = f"{viewed_questions},{fio}"
    resp.set_cookie(sheet_name, viewed_questions)
    return resp


if __name__ == "__main__":
    app.run(debug=True)
