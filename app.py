from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_migrate import Migrate

app = Flask(__name__)
application = app
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "ontheWall.db"))

app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///urmentor.db'

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

#Create db model
class URMentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        netID = request.form["inputNetID"]
        new_name = URMentor(name=netID)
        try:
            db.session.add(new_name)
            db.session.commit()
            return redirect('/login')
        except:
            return "error adding user to db"
    else:
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
