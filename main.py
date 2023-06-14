from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import db_config
from datetime import date, datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
UPLOAD_FOLDER = 'uploads'  # Relative path for the upload folder
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)

# init_db
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.hostname}:{db_config.port}/{db_config.db}'
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SECRET_KEY'] = b'\xef\x01w8\xcd\xe5\xf3!\xc1\xc2\x81k\x12\n\xd7P'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
db = SQLAlchemy(app)

with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine)
    # print(Base.classes.keys())
    db_table = {
        'admin': Base.classes.admin,
        'applicant': Base.classes.applicant,
        'apply': Base.classes.apply,
        'company': Base.classes.company,
        'events': Base.classes.events,
        'employs': Base.classes.employs,
        'participate': Base.classes.participate,
        'job': Base.classes.job,
        'resume': Base.classes.resume,
        'sponse': Base.classes.sponse
    }

    db_session = Session(db.engine, future=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Access denied because you are not logged in or logged in with an unprivileged account.'


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('front_page'))
    else:
        return render_template("hero.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_resume_url(resume_url):
    db.session.add(db_table['resume'](
       resume_url = resume_url))
    db.session.commit()


def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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


def db_add_company(form: dict):
    company_name = form['company_name']
    address = form['address']
    phone = form['phone']
    website = form['website']
    category = form['category']
    db.session.add(db_table['company'](
        company_name=company_name, address=address, phone=phone, website=website, category=category))
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
        print(request.form)
        if request.form['acc_type']=='ind':
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
        elif request.form['acc_type']=='com':
            # TODO: add company login here
            com_name = request.form['email']
            password = request.form['password']
            res = db.session.query(db_table['company']).filter(
                db_table['company'].company_name == com_name and db_table['company'].password == password).all()
            
            if(res.count()==1):
                # TODO: Authorize the user
                return redirect(url_for('company_frontPage'))

        return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/front_page")
@login_required
def front_page():
    if current_user.is_authenticated:
        jobs = db.session.query(db_table['job']).join(db_table['company']).all()
        return render_template("front_page.html", jobs=jobs)
    else:
        return login_manager.unauthorized()


@app.route("/modify_data", methods=['GET', 'POST'])
@login_required
def modify_data():
    if current_user.is_authenticated:
        if request.method == 'POST':
            db_update_user(current_user.id, request.form)
            return redirect(url_for('front_page'))
        else:
            return render_template("modify_data.html")
    else:
        return login_manager.unauthorized()


@app.route("/view_data")
@login_required
def view_data():
    if current_user.is_authenticated:
        data = db.session.query(db_table['applicant']).filter_by(applicant_id=current_user.id).first()
        applications = db.session.query(db_table['apply']).filter_by(applicant_id=current_user.id).all()
        return render_template("view_data.html", data=data, applications=applications)
    else:
        return login_manager.unauthorized()


@app.route("/company_register", methods=['GET', 'POST'])
def company_register():
        if request.method == 'POST':
            db_add_company(request.form)
            return redirect(url_for('company_frontPage'))
        else:
            return render_template("company_register.html")

@app.route("/company_frontPage")
def company_frontPage():
    # TODO: change 1 to user.id
    jobs = db.session.query(db_table['job']).join(db_table['company']).filter(db_table['company'].company_id == 1).all()
    return render_template("company_frontPage.html", jobs=jobs)


@app.route("/apply_page/<int:job_id>", methods=['GET', 'POST'])
@login_required
def apply_page(job_id):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_folder = os.path.join(app.root_path, 'uploads', request.remote_addr)
            os.makedirs(user_folder, exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            save_resume_url(file_path)
            uploaded_file(filename)
            print("上傳成功")
        resume_id = db.session.query(db_table['resume']).filter_by(resume_url=file_path).first().resume_id
        print(resume_id)
        db.session.add(db_table['apply'](
            applicant_id=int(
                current_user.id), job_id=job_id, resume_id=resume_id, state="processing", date=datetime.now()))
        db.session.commit()
        return redirect(url_for('front_page'))
    else:
        return render_template("apply_page.html")


@app.route("/company_info/<int:company_id>")
@login_required
def company_info(company_id):
    if current_user.is_authenticated:
        company = db.session.query(db_table['company']).filter_by(company_id=company_id).first()
        return render_template("company_info.html", company=company)
    else:
        return login_manager.unauthorized()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/event_page")
@login_required
def event_page():
    if current_user.is_authenticated:
        events = db.session.query(db_table['events']).all()
        sponsors = db.session.query(
            db_table['sponse'], db_table['events'], db_table['company']).filter(
            db_table['sponse'].company_id == db_table['company'].company_id).filter(
            db_table['sponse'].event_id == db_table['events'].event_id).all()
        for s in sponsors:
            print(dir(s[0]))
        return render_template("event_page.html", events=events, sponsors=sponsors)
    else:
        return login_manager.unauthorized()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)