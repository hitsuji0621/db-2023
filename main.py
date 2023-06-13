from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import db_config


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
def hello():
    return render_template("hero.html")

def db_add_user(req: dict):
    req.form['birthday']
    req.form['name']
    req.form['phone']
    req.form['gender']

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        db_add_user(request.form)
        return request.form
    else:
        return render_template("register.html")
    

@app.route("/login")
def login():
    return render_template("login.html")


if __name__=='__main__':
    app.run(host="0.0.0.0")