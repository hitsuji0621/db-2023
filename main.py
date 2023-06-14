from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import db_config
from datetime import date

# This is a sample Python script.

app = Flask(__name__)
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# init_db
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.hostname}:{db_config.port}/{db_config.db}'
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SECRET_KEY'] = b'\xef\x01w8\xcd\xe5\xf3!\xc1\xc2\x81k\x12\n\xd7P'
db = SQLAlchemy(app)

with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine)
    print(Base.classes.keys())
    db_table = {
        'admin': Base.classes.admin,
        'applicant': Base.classes.applicant,
        'apply': Base.classes.apply,
        'company': Base.classes.company,
        'events': Base.classes.events,
        'employs': Base.classes.employs,
        'participate': Base.classes.participate,
        'submit': Base.classes.submit,
        'job': Base.classes.job
    }

    db_session = Session(db.engine, future=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Access denied because you are not logged in or logged in with an unprivileged account.'


@app.route("/")
def home():
    return render_template("hero.html")


def db_add_user(form: dict):
    birthday = form['birthday'] if form['birthday'] != '' else str(date.today())
    name = form['name']
    phone = form['phone']
    gender = form['gender']
    email = form['email']
    pwd = form['password']
    db.session.add(db_table['applicant'](
         email=email, password=pwd, zh_name=name, phone=phone, gender=gender, birthday=birthday))
    db.session.commit()


def db_update_user(applicant_id, form: dict):
    user = db.session.query(db_table['applicant']).get(applicant_id)

    if user:
        user.birthday = form.get('birthday', user.birthday)
        user.zh_name = form.get('name', user.zh_name)
        user.phone = form.get('phone', user.phone)
        user.gender = form.get('gender', user.gender)
        user.email = form.get('email', user.email)
        user.password = form.get('password', user.password)
        db.session.commit()


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        db_add_user(request.form)

        return redirect(url_for('home'))
    else:
        return render_template("register.html")


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(applicant_id):
    applicant = User()
    applicant.id = applicant_id
    return applicant


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        for t in db.session.query(db_table['applicant']).all():
            if email == t.email and password == t.password:
                user = User()
                user.id = t.applicant_id
                login_user(user)
                flash('Logged in successfully.')
                print('Logged in successfully.')
                return redirect(url_for('front_page'))

        return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/front_page")
def front_page():
    return render_template("front_page.html")


@app.route("/modify_data", methods=['GET', 'POST'])
def modify_data():
    if request.method == 'POST':
        db_update_user(current_user.id, request.form)
        return redirect(url_for('front_page'))
    else:
        return render_template("modify_data.html")


app.run(host="0.0.0.0", debug=True)
