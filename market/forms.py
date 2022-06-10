from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    # Si o si tiene que empezar con validate_ asi funciona automaticamente
    def validate_username(self, username_to_check): 
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email already exists! Please try a different email')

    username = StringField(label='Username:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Adress:', validators=[
                        Email(), DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[
                               Length(min=8), DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[
                               EqualTo('password_1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')