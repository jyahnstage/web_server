from flask import Flask, render_template, request, redirect, session, url_for
from data import Articles
from mysql import Mysql
import config
import pymysql
from datetime import timedelta
from functools import wraps
app = Flask(__name__)
mysql = Mysql(password=config.PASSWORD)
# app.secret_key = 'eungok'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
app.config['SESSION_PERMANENT'] = False
app.config['SEESION_TYPE'] = 'filesystem'

def is_logged_in(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'is_logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap


@app.route('/', methods=['GET', 'POST'])
# @is_logged_in
def index():
#     if request.method == "GET":
#         os_info = dict(request.headers)
#         print(os_info)
#         name = request.args.get("name")
#         print(name)
#         hello = request.args.get("hello")
#         print(hello)
#         return render_template('index.html', header=f'{name}님 {hello}!')
    
#     elif request.method == "POST":
#         data = request.form.get("name")
#         data2 = request.form["age"]
#         print(data)
#         return render_template('index.html', header="hello")
        # print(session['is_logged_in'])
        return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('hello.html')
    
    elif request.method == "POST":
        name = request.form['name']
        hello = request.form['hello']
        return render_template('index.html', name=name, hello=hello)
    
@app.route('/list', methods=['GET', 'POST'])
def list():
        if request.method == 'GET':
            data = Articles()
            result = mysql.get_data()
            # print(result)
            return render_template('list.html', data = result)
        
        elif request.method == "POST":
            title = request.form['title']
            desc = request.form['desc']
            author = request.form['author']
            result = mysql.insert_list(title, desc, author)
            print(result)
            return redirect('/list')

@app.route('/create_list', methods=['GET', 'POST'])
def create_list():
        if request.method == 'GET':
            return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(username, email, phone, password)
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s'
        curs.execute(sql, email)

        rows = curs.fetchall()  
        print(rows)
        if rows:
            return render_template('register.html', data=1)
        else:
            result = mysql.insert_user(username, email, phone, password)
            print(result)
            return redirect('/login')
        
    
    elif request.method == "GET":
        return render_template('register.html', data=0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s'
        curs.execute(sql, email)

        rows = curs.fetchall()  
        print(rows)
        if rows:
            result = mysql.verify_password(password, rows[0][4])
            if result:
                session['is_logged_in'] = True
                session['username'] = rows[0][1]
                return redirect('/')
                # return render_template('index.html', is_logged_in = session['is_logged_in'], username = session['username'])
            else:
                return redirect('/login')
        else:
            return render_template('login.html')

@app.route('/logout')       
def logout():
    session.clear()
    return redirect('/')

@app.route('/edit/<ids>')
def edit(ids):
    return ids

@app.route('/delete/<ids>')
def delete(ids):
    return ids


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'eungok'
    app.run(debug = True)

