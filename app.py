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

@app.route('/createMentee1')
def createMentee1():
    return render_template("createMentee1.html")

@app.route('/createMentee2')
def createMentee2():
    return render_template("createMentee2.html")

@app.route('/createMentor1')
def createMentor1():
    return render_template("createMentor1.html")

@app.route('/createMentor2')
def createMentor2():
    return render_template("createMentor2.html")

@app.route('/createMentor3')
def createMentee3():
    return render_template("createMentor3.html")

@app.route('/menteeMain')
def menteeMain():
    return render_template("menteeMain.html")

@app.route('/mentorMain')
def mentorMain():
    return render_template("mentorMain.html")

@app.route('/findMatch')
def findMatch():
    return render_template("findMath.html")

@app.route('/matchResult')
def matchResult():
    return render_template("matchResult.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")
