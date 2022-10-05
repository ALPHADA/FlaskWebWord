from flask import Flask, request, redirect, render_template
import random

app = Flask(__name__)

words = [
    {'id': 1, 'english':'whale', 'korean':'고래'},
    {'id': 2, 'english':'age', 'korean':'나이'},
    {'id': 3, 'english':'air', 'korean':'공기'},
    {'id': 4, 'english':'ago', 'korean':'이전에'},
    {'id': 5, 'english':'coding', 'korean':'코딩'},
]
nextId = len(words) + 1

def template(content, id=None):
    detailHtml = ''
    if id != None:
        detailHtml = f'''
        <ul>
        <li><a href="/update/{id}/">update</a></li>
        <li><form action="/delete/{id}/" method="POST">
            <input type="submit" value="delete"></form></li>
        </ul>
        '''
    html = f'''<html>
    <head></head>
    <body cz-shortcut-listen="true">
        <h1><a href="/">단어장</a></h1>
        <ol>
            <li><a href="/random/">random</a></li>
            <li><a href="/reads/">list</a></li>
            <li><a href="/create/">create</a></li>
        </ol>
        {content}
        {detailHtml}
    </body></html>'''
    return html

@app.route('/')
def index():
    titleString = 'Whalecoding 단어장'
    contentString = '환영합니다. 하하'
    return render_template('index.html', title=titleString, content=contentString)
    
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        global nextId
        english = request.form['english']
        korean = request.form['korean']
        newword = {'id':nextId, 'english':english, 'korean':korean}
        words.append(newword)
        nextId += 1
        return redirect(f'/read/{newword["id"]}/')

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
        return render_template('update.html', id=id, english=english, korean=korean)
    elif request.method == 'POST':
        redirectId = 0
        for word in words:
            if id == word['id']:
                redirectId = id
                word["english"] = request.form['english']
                word["korean"] = request.form['korean']
                break

        return redirect(f'/read/{redirectId}/')

@app.route('/reads/')
def reads():
    return render_template('list.html', words=words)

@app.route('/read/<int:id>/')
def read(id):
    english = ''
    korean = ''
    for word in words:
        if id == word['id']:
            english = word['english']
            korean = word['korean']
            break
        
    return render_template('read.html', id=id, english=english, korean=korean)


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for word in words:
        if id == word['id']:
            words.remove(word)
            break
    
    return redirect(f'/reads/')

@app.route('/random/')
def randomWord():
    sample = random.sample(words, 4) 
    # [
    # {'id': 5, 'english':'coding', 'korean':'코딩'},
    # {'id': 1, 'english':'whale', 'korean':'고래'},
    # {'id': 2, 'english':'age', 'korean':'나이'},
    # {'id': 3, 'english':'air', 'korean':'공기'},
    # ]
    answer = sample[0]
    liTag = ''
    random.shuffle(sample)
    for word in sample:
        liTag += f'<li>{word["korean"]}</li>'
    
    content = f'''<h2>{answer["english"]}</h2>
        <ol>
        {liTag}
        </ol>
        <p>
        <details><summary>정답</summary>
        {answer["english"]}, {answer["korean"]}</details>
        </p> <br/>
        <a href="/random/">next</a>'''
    return template(content)






if __name__ == '__main__':
    app.run(debug=True)
