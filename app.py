from chatbot import chatbot
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import mysql.connector
import os
import openai

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.static_folder = 'static'

openai.api_key = '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'

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

# database connectivity
conn = mysql.connector.connect(
    host='localhost', port='3306', user='root', passwd='', database='register')
cur = conn.cursor()

# Google recaptcha - site key : 6LdbAx0aAAAAAANl04WHtDbraFMufACHccHbn09L
# Google recaptcha - secret key : 6LdbAx0aAAAAAMmkgBKJ2Z9xsQjMD5YutoXC6Wee


@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    # return render_template("login.html")    change if it doesn\t work
    return render_template("login.html")


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for specific username and password values
    if email == 'admin@gmail.com' and password == '123':
        return redirect('http://localhost/phpmyadmin/index.php?route=/sql&db=register&table=users&pos=0')

    cur.execute(
        """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cur.fetchall()
    if len(users) > 0:
        session['id'] = users[0][0]
        flash('You were successfully logged in')
        return redirect('/index')
    else:
        flash('Invalid credentials !!!')
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    #cur.execute("UPDATE users SET password='{}'WHERE name = '{}'".format(password, name))
    cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(
        name, email, password))
    conn.commit()
    cur.execute(
        """SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cur.fetchall()
    flash('You have successfully registered!')
    session['id'] = myuser[0][0]
    return redirect('/index')


@app.route('/suggestion', methods=['POST'])
def suggestion():
    email = request.form.get('uemail')
    suggesMess = request.form.get('message')

    cur.execute("""INSERT INTO  suggestion(email,message) VALUES('{}','{}')""".format(
        email, suggesMess))
    conn.commit()
    flash('You suggestion is succesfully sent!')
    return redirect('/index')


@app.route('/add_user', methods=['POST'])
def register():
    return redirect('/register')


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    try:
        if userText.startswith("+"):
            prompt = userText[1:]
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            return image_url
    except:
        return "fbi is on the way good luck"
    else:
        return str(chatbot.get_response(userText))


if __name__ == "__main__":
    # app.secret_key=""
    app.run()
