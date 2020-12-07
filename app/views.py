from app import app
from app import db
from app.models import Icon, About, Project, Area, Servis, User
from flask import render_template,redirect,request,url_for,session,logging, flash
from app.forms import RegisterForm, LoginForm, UpdateAccountForm
from app import bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def appIndex():
    alldata=Icon.query.all()
    allarea=Area.query.all()
    return render_template('app/index.html', allicons=alldata, alldatas=allarea)

@app.route('/industry/about')
def appabout():
    alldata=Icon.query.all()
    allabout=About.query.all()
    return render_template('app/about.html', allicons=alldata, alldatas=allabout)

@app.route('/industry/projects')
def appprojects():
    alldata=Project.query.all()
    return render_template('app/projects.html', allprojects=alldata)

@app.route('/industry/servis')
@login_required
def appservis():
    return render_template('app/servis.html')

@app.route('/industry/servis/add', methods=['POST'])
def addappservis():
    if request.method == 'POST':
        subject=request.form['subject']
        name=request.form['name']
        surname=request.form['surname']
        email=request.form['email']
        phone=request.form['phone']
        street=request.form['street']
        country=request.form['country']
        city=request.form['city']
        text=request.form['text']
        mydata=Servis(subject, name, surname, email, phone, street, country, city, text)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('appservis'))


@app.route('/industry/contact')
def appcontact():
    return render_template('app/contact.html')


@app.route("/hesabım", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.company = form.company.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Hesab Məlumatlarınız Yeniləndi!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.company.data = current_user.company
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    
    return render_template('app/account.html', title='Hesabım', form=form)


@app.route('/industry/register', methods=['GET', 'POST'])
def appregister():
    if current_user.is_authenticated:
        return redirect(url_for('appIndex'))
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(name=form.name.data, surname=form.surname.data, company=form.company.data, email=form.email.data, phone=form.phone.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Qeydiyyat uğurla başa çatdı, giriş edə bilərsiniz', 'success')
        return redirect(url_for('applogin'))
    return render_template('app/register.html', title="Qeydiyyat Forumu", form = form)
    


@app.route('/industry/login', methods=['GET', 'POST'])
def applogin():
    if current_user.is_authenticated:
        return redirect(url_for('appIndex'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_level=request.args.get('next')
            return redirect(next_level) if next_level else redirect(url_for('appIndex'))
        else:
            flash('Giriş uğursuz oldu, zəhmət olmasa mail və şifrənizi yoxlayın', 'danger')
    return render_template('app/login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def applogout():
    logout_user()
    return redirect(url_for('appIndex'))

