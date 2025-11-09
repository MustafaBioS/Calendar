import uuid
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from dotenv import load_dotenv
import os

# Initialization

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

load_dotenv()
secret = os.getenv("Secret_Key")
app.config['SECRET_KEY'] = secret

db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False ,unique=True)
    password = db.Column(db.String(128), nullable=False)

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(12), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:12])
    name = db.Column(db.String(100))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.String(50))

    calendar = db.relationship('Calendar', backref=db.backref('events', lazy=True))

# Routes

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    return render_template("index.html")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        name = request.form.get("cn")
        new_calendar = Calendar(name=name)
        db.session.add(new_calendar)
        db.session.commit()
        return redirect(url_for("view", public_id=new_calendar.public_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        loguser = request.form.get("loguser")
        logpass = request.form.get("logpass")

        signuser = request.form.get("signuser")
        signpass = request.form.get("signpass")
        signcon = request.form.get("signcon")

        if signuser and signpass:
            if signpass == signcon:
                hashed_pw = bcrypt.generate_password_hash(signpass).decode("utf-8")
                new_user = Users(username=signuser, password=hashed_pw)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    flash("Account Created Successfully", 'success')
                    return redirect(url_for('home'))
                except Exception as e:
                    db.session.rollback()
                    flash("Username Already Taken", "fail")
                    return redirect(url_for('login'))
            else:
                flash("Passwords Do Not Match", 'fail')

        if loguser and logpass:
            user = Users.query.filter_by(username=loguser).first()
            if user is None:
                flash("User Not Found", 'fail')
                return redirect(url_for('login'))
            if bcrypt.check_password_hash(user.password, logpass):
                login_user(user)
                flash("Logged In Successfully", 'success')
                return redirect(url_for("home"))
            else:
                flash("Incorrect Username or Password", 'fail')
                return redirect(url_for("login"))
            
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged Out Successfully", 'success')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/delete')
def delete():
    user = Users.query.filter_by(username=current_user.username).first()
    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()
        flash("Account Deleted Successfully", 'success')
        return redirect(url_for('home'))

# Run

if __name__ == '__main__':
    app.run(debug=True)