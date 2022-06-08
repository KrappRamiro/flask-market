from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(label='Username:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Adress:', validators=[
                        Email(), DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[
                               Length(min=8), DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[
                               EqualTo('password_1'), DataRequired()])
    submit = SubmitField(label='Create Account')
