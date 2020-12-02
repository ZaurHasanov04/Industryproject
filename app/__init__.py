from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__,template_folder='../templates',static_folder='../static')
db=SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./industry.db"
db = SQLAlchemy(app)
from app import models
from app import views

from admin import models
from admin import views

db.create_all()