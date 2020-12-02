from app import app
from app import db
from flask import render_template,redirect,request,url_for

class Icon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),  nullable=False)
    text = db.Column(db.String(255),  nullable=False)
    def __init__(self, title, text):
        self.title=title
        self.text=text

class About(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text=db.Column(db.String(255), nullable=False)
    def __init__(self, title, text):
        self.title=title
        self.text=text

class Project(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category=db.Column(db.String(255), nullable=False)
    text=db.Column(db.Text(), nullable=False)
    photoURL=db.Column(db.String())
    def __init__(self, title, category, text, photoURL):
        self.title=title
        self.category=category
        self.text=text
        self.photoURL=photoURL

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),  nullable=False)
    text = db.Column(db.String(255),  nullable=False)
    def __init__(self, title, text):
        self.title=title
        self.text=text


