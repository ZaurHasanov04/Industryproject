from app import app
from app import models
from admin import Icon, About, Project, Area
from flask import render_template,redirect,request,url_for


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
def appservis():
    return render_template('app/servis.html')

@app.route('/industry/contact')
def appcontact():
    return render_template('app/contact.html')

@app.route('/industry/login')
def applogin():
    return render_template('app/login.html')

@app.route('/industry/register')
def appregister():
    return render_template('app/register.html')