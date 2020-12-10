import os
import smtplib
import secrets
from flask import render_template,redirect,request,url_for,session,logging, flash
from app import app, db, mail,bcrypt
from app.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.models import Icon, About, Project, Area, Servis, User, Contact
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

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
    alldata=Icon.query.all()
    all=About.query.all()
    return render_template('app/servis.html', allicons=alldata, about=all)

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

@app.route('/contact/add', methods=['POST'])
def addcontact():
    if request.method == 'POST':
        namesurname=request.form['namesurname']
        email=request.form['email']
        subject=request.form['subject']
        text=request.form['text']
        mydata=Contact(namesurname, email,  subject, text)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('appIndex'))


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



# Reset Password

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Şifrə Yeniləmə Sorğusu', sender='zaurqwerty@gmail.com', recipients=[user.email])
    msg.body = f'''Şifrənizi yeniləmək üçün aşağıdakı linkə daxil ola bilərsiz:
{url_for('reset_token', token=token, _external=True)}
Əgər siz belə bir sorğu göndərməmisinizsə narahat olmayın, bu maili silə bilərsiz, hesabınızla bağlı heç bir dəyişiklik edilməyəcək.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email ünvanınıza şifrə yeniləməsi üçün link göndərildi.', 'info')
        return redirect(url_for('applogin'))
    return render_template('app/resetform.html', title='Şifrəni Yeniləmək Üçün Sorğu Göndər', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Şifrəniz yeniləndi! İndi hesabınıza daxil ola bilərsiniz.', 'success')
        return redirect(url_for('applogin'))
    return render_template('app/resettoken.html', title='Şifrəni Yenilə', form=form)