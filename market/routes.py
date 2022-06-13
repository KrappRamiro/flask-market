from market import app
from flask import flash, render_template, redirect, url_for
from market.models import User, Item
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user


@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')


@app.route('/market/')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password_1.data)  # i think this calls the @property password and the setter in models.py
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error, with creating an user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm() #Consigo mi form de forms.py
    if form.validate_on_submit():  # validate_on_submit validates that all the info is valid
        # Verify if the users exists
        attempted_user = User.query.filter_by(username = form.username.data).first()
        # Get the user that is equal to the username in the form
        # AND if the user exists, verify that the password is correct
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user) #Se loggea al usuario usando el modulo flask_login
            flash(
                f"Hello {attempted_user.username}! You are logged in!", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password do not match. Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout_page():
    logout_user() #Esto es parte de flask_login, funciona porque declare en __init__.py que se use flask_login
    flash("Successfully logged out!", category='info')
    return redirect(url_for('home_page'))