from flask import Flask, request, redirect
import random


words = [
    {'id': 1, 'english': 'whale', 'korean': '고래'},
    {'id': 2, 'english': 'coding', 'korean': '코딩'},
    {'id': 3, 'english': 'word', 'korean': '단어'},
    {'id': 4, 'english': 'create', 'korean': '생성하다'},
    {'id': 5, 'english': 'update', 'korean': '수정하다'},
    {'id': 6, 'english': 'delete', 'korean': '삭제하다'},
    {'id': 7, 'english': 'age', 'korean': '연령'},
    {'id': 8, 'english': 'air', 'korean': '공기'},
    {'id': 9, 'english': 'ago', 'korean': '이전에'}
]
nextId = 10

app = Flask(__name__)

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    style = '''body,h1,h2,h3,h4,h5 {font-family: "Raleway", sans-serif}
    body {margin: 0 auto; width: 480px;}'''
    return f'''<!doctype html>
    <html>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
        <style>
            {style}
        </style>
        <body  class="w3-light-grey">
            <h1><a href="/">단어장</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    liTags += '<li><a href="/random/">random</a></li>'
    liTags += '<li><a href="/reads/">list</a></li>'
    liTags += '<li><a href="/create/">create</a></li>'
    return liTags

def getWords():
    liTags = ''
    for word in words:
        liTags = liTags + f'<li><a href="/read/{word["id"]}/">{word["english"]}</a> {word["korean"]} </li>'

    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Whalecoding 단어장</h2>환영합니다.')

@app.route('/random/')
def randomWord():
    english = ''
    datas = random.sample(words, 4)
    english = datas[0]['english']
    korean = datas[0]['korean']
    liTags = ''
    random.shuffle(datas)
    for word in datas:
        liTags = liTags + f'<li>{word["korean"]}</li>'

    answer = f'''<details>
   <summary>정답!</summary>
   <p>'{english} {korean}'</p>
</details>'''
    nextButton = '<br><a href="/random/">next</a>'
    return template(getContents(), f'<h2>영어 랜덤 단어</h2><h2>{english}</h2>{liTags}{answer}{nextButton}')

@app.route('/reads/')
def reads():
    return template(getWords(), '')

@app.route('/read/<int:id>/')
def read(id):
    english = ''
    korean = ''
    for word in words:
        if id == word['id']:
            english = word['english']
            korean = word['korean']
            break
    return template(getContents(), f'<h2>{english}</h2>{korean}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="english" placeholder="english"></p>
                <p><textarea name="korean" placeholder="korean"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        newword = {'id': nextId, 'english': english, 'korean': korean}
        words.append(newword)
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET': 
        english = ''
        korean = ''
        for word in words:
            if id == word['id']:
                english = word['english']
                korean = word['korean']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="english" placeholder="english" value="{english}"></p>
                <p><textarea name="korean" placeholder="korean">{korean}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        for word in words:
            if id == word['id']:
                word['english'] = english
                word['korean'] = korean
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for word in words:
        if id == word['id']:
            words.remove(word)
            break
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
