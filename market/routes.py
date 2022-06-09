from market import app
from flask import flash, render_template, redirect, url_for
from market.models import User, Item
from market.forms import RegisterForm
from market import db


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
                              password_hash=form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error, with creating an user: {err_msg}', category='danger')
    return render_template('register.html', form=form)
