from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager, UserMixin
from datetime import datetime

app = Flask(__name__)
application = app
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "ontheWall.db"))

app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///urmentor.db'

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Create db model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netID = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(100), unique = True, nullable=False)
    fullName = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100))
    mentor = db.Column(db.Boolean)
    major = db.Column(db.String(50))
    year = db.Column(db.String(50))
    location = db.Column(db.String(100))
    interestID = db.Column(db.Integer, db.ForeignKey('interest.id'))
    mentorID = db.Column(db.Integer, unique=True)
    # phone = db.Column(db.)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.id

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique = True)
    users = db.relationship('User', backref='interest')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        netID = request.form["inputNetID"]
        email = request.form["email"]
        fullName = request.form["fullName"]
        password = request.form["password"]
        user = User.query.filter_by(netID=netID).first()
        if user:
            flash("Seems like you already have an account.", "info")
            return redirect('/register')
        new_user = User(netID=netID, email=email, fullName=fullName, password_hash=generate_password_hash(password, method='sha1'))
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return "error adding user to db"
    else:
        return render_template("register.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        netID = request.form.get('inputNetID')
        password = request.form.get('password')
        user = User.query.filter_by(netID=netID).first()
        if not user or not user.verify_password(password):
            flash("Please check your login details and try again.")
            return redirect('/login')
        login_user(user)
        return redirect('/welcome')
        # user = User

@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if request.method == 'POST':
        response = request.form.get('ment')
        userId = current_user.id
        user = User.query.filter_by(id=userId).first()
        if response == 'Mentor':
            user.mentor == True
            db.session.commit()
            return redirect('/createMentor1')
        else:
            user.mentor == False
            db.session.commit()
            return redirect('/createMentee1')
    else:
        return render_template("welcome.html")

@app.route('/createMentee1', methods=['GET','POST'])
@login_required
def createMentee1():
    if request.method == 'POST':
        userId = current_user.id
        user = User.query.filter_by(id=userId).first()
        major = request.form.get('major')
        year = request.form.get('year')
        location = request.form.get('location')
        try:
            user.major = major
            user.year = year
            user.location = location
            db.session.commit()
            return redirect('/createMentee2')
        except:
            return "error adding user to db"
    else:
        return render_template("createMentee1.html")

@app.route('/createMentee2')
@login_required
def createMentee2():
    return render_template("createMentee2.html")

@app.route('/createMentor1', methods=['GET', 'POST'])
@login_required
def createMentor1():
    if request.method == 'POST':
        education = request.form.get('education')
        semester = request.form.get('inlineRadioOptions')
        if semester == 'true':
            return redirect('/createMentor2')
        else:
            return 'Sorry you are not eligible to be a mentor'
    else:
        return render_template("createMentor1.html")

@app.route('/createMentor2', methods=['GET', 'POST'])
@login_required
def createMentor2():
    if request.method == 'POST':
        userId = current_user.id
        user = User.query.filter_by(id=userId).first()
        major = request.form.get('major')
        year = request.form.get('year')
        location = request.form.get('location')
        try:
            user.major = major
            user.year = year
            user.location = location
            db.session.commit()
            return redirect('/createMentor3')
        except:
            return "error adding user to db"
    else:
        return render_template("createMentor2.html")

@app.route('/createMentor3', methods=['GET', 'POST'])
@login_required
def createMentee3():
    if request.method == "POST":
        return redirect('/mentorMain')
    return render_template("createMentor3.html")

@app.route('/menteeMain')
@login_required
def menteeMain():
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    return render_template("menteeMain.html", name=user.fullName)

@app.route('/mentorMain')
@login_required
def mentorMain():
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    return render_template("mentorMain.html", name=user.fullName)

@app.route('/findMatch')
@login_required
def findMatch():
    return render_template("findMath.html")

@app.route('/matchResult')
@login_required
def matchResult():
    return render_template("matchResult.html")

@app.route('/settings')
@login_required
def settings():
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    return render_template("settings.html", netID=user.netID, year=user.year, email=user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
