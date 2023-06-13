from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import db_config
from datetime import date

app = Flask(__name__)

# init_db
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.hostname}:{db_config.port}/{db_config.db}'
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
db=SQLAlchemy(app)


with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine)
    print(Base.classes.keys())
    db_table={
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

@app.route("/")
def home():
    return render_template("hero.html")

def db_add_user(form: dict):
    birthday=form['birthday'] if form['birthday']!='' else str(date.today())
    name=form['name']
    phone=form['phone']
    gender=form['gender']
    email=form['email']
    pwd=form['password']
    db.session.add(db_table['applicant'](
        applicant_id=name, email=email, password=pwd, zh_name=name, phone=phone, gender=gender, birthday=birthday))
    db.session.commit()

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        print(request.form)
        db_add_user(request.form)

        return redirect(url_for('home'))
    else:
        return render_template("register.html")
    

@app.route("/login")
def login():
    return render_template("login.html")


if __name__=='__main__':
    app.run(host="0.0.0.0")