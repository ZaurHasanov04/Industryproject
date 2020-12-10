from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app, db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


class Servis(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    subject=db.Column(db.String(255), nullable=False)
    name=db.Column(db.String(100), nullable=False)
    surname=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(150), nullable=False)
    phone=db.Column(db.String(150), nullable=False)
    street=db.Column(db.String(255), nullable=False)
    country=db.Column(db.String(200), nullable=False)
    city=db.Column(db.String(200), nullable=False)
    text=db.Column(db.Text(), nullable=False)
    def __init__(self, subject, name, surname, email, phone, street, country, city, text):
        self.subject=subject
        self.name=name
        self.surname=surname
        self.email=email
        self.phone=phone
        self.street=street
        self.country=country
        self.city=city
        self.text=text


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    surname=db.Column(db.String(100), nullable=False)
    company=db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(150), nullable=False)
    phone=db.Column(db.String(150), nullable=False)
    password=db.Column(db.String(50), nullable=False)
    def __init__(self, name, surname, company, email, phone, password ):
        self.name=name
        self.surname=surname
        self.company=company
        self.email=email
        self.phone=phone
        self.password=password

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def is_active(self):
       return True


class Contact(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    namesurname=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(150), nullable=False)
    subject=db.Column(db.String(255), nullable=False)
    text=db.Column(db.Text(), nullable=False)
    def __init__(self, namesurname,  email, subject, text):
        self.namesurname=namesurname
        self.email=email
        self.subject=subject
        self.text=text



class Logo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    photoURL=db.Column(db.String())
    def __init__(self,  photoURL):
        self.photoURL=photoURL
    

    