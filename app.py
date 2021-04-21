from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)
application = app

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/createMentee')
def createMentee():
    return render_template("createMentee.html")
