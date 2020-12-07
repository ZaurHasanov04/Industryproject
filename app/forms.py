from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from passlib.hash import sha256_crypt
from app.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), validators.Email(message="Xahiş edirik mailinizi düzgün yazın")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Hesabıma Daxil Ol', render_kw={"style": "width:100%;"})



class RegisterForm(FlaskForm):
    name= StringField("Adınızı yazın", validators=[validators.Length(min=3, max=25) , validators.DataRequired(message="Bu xana boş buraxıla bilməz")])
    surname= StringField("Soyadınızı yazın", validators=[validators.Length(min=5, max= 25), validators.DataRequired(message="Bu xana boş buraxıla bilməz")])
    company= StringField("İşlədiyiniz Şirkətin adı")
    email=StringField("Elektron poçtunuzu yazın", validators=[validators.Email(message="Xahiş edirik mail ünvanınızı doğru yazın")])
    phone=StringField("Nömrənizi yazın",validators=[validators.DataRequired(message="Telefon nömrənizi yazın"), validators.Length(min=7, max=16)])
    password=PasswordField("Şifrənizi yazın:", validators=[validators.DataRequired(message="Xahiş edirik şifrənizi yazın"), validators.Length(min=8, max=80, message="Sifre sayi 8 den boyuk olmalidi"),
    validators.EqualTo(fieldname="confirm", message="Şifrəniz uyğun gəlmir")
    ])
    confirm=PasswordField("Şifrənizi təsdiq edin")
    def validate_username(self, phone):

        user = User.query.filter_by(phone=phone.data).first()

        if user:
            raise ValidationError('Daxil etdiyiniz nömrə artıq istifadə olunub. Zəhmət olmasa, fərqli nömrə daxil edin. ')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Daxil etdiyiniz Email artıq istifadə olunub. Zəhmət olmasa, fərqli Email daxil edin.')






class UpdateAccountForm(FlaskForm):
    name = StringField('İstifadəçi Adı', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Ad', validators=[DataRequired(), Length(min=2, max=20)])
    company = StringField('İş yeriniz')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone=StringField("Nömrənizi yazın",validators=[validators.DataRequired(message="Telefon nömrənizi yazın"), validators.Length(min=7, max=16)])
    
    
    

    def validate_username(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()

            if user:
                raise ValidationError('Daxil etdiyiniz nömrə artıq istifadə olunub. Zəhmət olmasa, nömrə daxil edin.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Daxil etdiyiniz Email artıq istifadə olunub. Zəhmət olmasa, fərqli Email daxil edin.')