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
    password_hash = db.Column(db.String(100), nullable=False)
    mentor = db.Column(db.Boolean)
    major = db.Column(db.String(50))
    year = db.Column(db.String(50))
    location = db.Column(db.String(100))
    availability = db.Column(db.String(100))
    interests = db.relationship('Interest', backref='user')
    # mentorships = db.relationship('Mentorship', backref='user')
    # phone = db.Column(db.)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.id

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class Mentorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentorID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentor = db.relationship("User", foreign_keys=[mentorID])
    menteeID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentee = db.relationship("User", foreign_keys=[menteeID])

    accepted = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)
    # mentee = db.relationship("User", foreign_keys=[menteeID])

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
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    if request.method == 'POST':
        response = request.form.get('ment')
        if response == 'Mentor':
            user.mentor = True
            db.session.commit()
            return redirect('/createMentor1')
        else:
            user.mentor = False
            db.session.commit()
            return redirect('/createMentee1')
    else:
        if user.mentor == True:
            return redirect('/mentorMain')
        elif user.mentor == False:
            return redirect('/menteeMain')
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

@app.route('/createMentee2', methods=['GET', 'POST'])
@login_required
def createMentee2():
    if request.method == "POST":
        userId = current_user.id
        if request.form.get("Topic1"):
            new_interest = Interest(title=request.form.get("Topic1"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic2"):
            new_interest = Interest(title=request.form.get("Topic2"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic3"):
            new_interest = Interest(title=request.form.get("Topic3"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic4"):
            new_interest = Interest(title=request.form.get("Topic4"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic5"):
            new_interest = Interest(title=request.form.get("Topic5"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic6"):
            new_interest = Interest(title=request.form.get("Topic6"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic7"):
            new_interest = Interest(title=request.form.get("Topic7"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic8"):
            new_interest = Interest(title=request.form.get("Topic8"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic9"):
            new_interest = Interest(title=request.form.get("Topic9"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        return redirect('/menteeMain')
    else:
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
        userId = current_user.id
        if request.form.get("Topic1"):
            new_interest = Interest(title=request.form.get("Topic1"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic2"):
            new_interest = Interest(title=request.form.get("Topic2"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic3"):
            new_interest = Interest(title=request.form.get("Topic3"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic4"):
            new_interest = Interest(title=request.form.get("Topic4"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic5"):
            new_interest = Interest(title=request.form.get("Topic5"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic6"):
            new_interest = Interest(title=request.form.get("Topic6"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic7"):
            new_interest = Interest(title=request.form.get("Topic7"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic8"):
            new_interest = Interest(title=request.form.get("Topic8"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        if request.form.get("Topic9"):
            new_interest = Interest(title=request.form.get("Topic9"), userID=userId)
            db.session.add(new_interest)
            db.session.commit()
        return redirect('/mentorMain')
    else:
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

    interests = Interest.query.filter_by(userID=userId)
    return render_template("mentorMain.html", name=user.fullName, interests=interests)

@app.route('/findMatch')
@login_required
def findMatch():
    userId = current_user.id
    user = User.query.filter_by(id=userId).first()
    interests, mentors, bestMentor = matchAlgorithm(user)
    # mentors = db.query(Interest, User).filter(User.id == Interest.UserID).filter(User.mentor == True).all()
    return render_template("findMatch.html", name=user.fullName, interests=interests, mentors=mentors, bestMentor=bestMentor)

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

# algorithms
def matchAlgorithm(user):
    mentorDict = {}
    bestMentor = 0
    menteeInterests = Interest.query.filter_by(userID=user.id)
    Interest.query.filter_by()
    # list of mentor IDs
    mentors = User.query.join(Interest).filter(User.mentor == True)
    # search through interests of the mentors and
    # keep count of how many interests in common
    for mentor in mentors:
        mentorID = mentor.id
        mentorInterests = Interest.query.filter_by(userID=mentorID)
        common = compareInterests(menteeInterests, mentorInterests)
        e = {mentorID: common}
        mentorDict.update(e)
    # print(mentorDict)
    # return mentor with the most interests in common
    for key in mentorDict:
        if mentorDict[key] > bestMentor:
            bestMentor = mentorDict[key]
    return menteeInterests, mentors, bestMentor

def compareInterests(interest1, interest2):
    common = 0
    for interest in interest1:
        if interest in interest2:
            common += 1
    return common
