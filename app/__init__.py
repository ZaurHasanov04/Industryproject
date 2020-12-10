import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
app=Flask(__name__,template_folder='../templates',static_folder='../static')



app.config['SECRET_KEY']='44804c67cdbda5452e3219b0f631f0cb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./industry.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='applogin'
login_manager.login_message_category='info'
login_manager.login_message='Zəhmət olmasa hesabınıza daxil olun'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from app import models
from app import views

from app import models
from admin import views

db.create_all()