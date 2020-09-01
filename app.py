from chatbot import chatbot
from flask import Flask, render_template, request,session,logging,url_for,redirect,flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)
app.static_folder = 'static'

conn=mysql.connector.connect(host='localhost',user='root',password='1234',database='register')
cur=conn.cursor()

@app.route("/index")
def home():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                  .format(email,password))
    users = cur.fetchall()
    if len(users)>0:
        session['email']=users[0][0]
        return redirect('/index')
    else:
        return redirect('/')
    # return "The Email is {} and the Password is {}".format(email,password)
    # return render_template('register.html')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cur.fetchall()
    session['email']=myuser[0][0]
    return redirect('/index')

@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    # app.secret_key=""
    app.run() 
