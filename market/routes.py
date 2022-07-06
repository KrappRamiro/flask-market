from market import app
from flask import flash, render_template, redirect, url_for, request
from market.models import User, Item
from market.forms import AddItemForm, RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home.html')


@app.route('/market/', methods=['GET', 'POST'])
@login_required  # This is from flask_login, its configured in __init__.py
def market_page():
    # We need to pass this to the template because we need to access the information in the modal
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    # When someone purchases an item, this happens
    # It gets the item, and it assigns it to the owner
    if request.method == "POST":
        # ---- Start of Purchase Item Logic ---------------------------------------------------
        # Este es el nombre que conseguimos del form
        purchased_item = request.form.get('purchased_item')
        # Este es un item de la base de datos
        purc_item_object = Item.query.filter_by(name=purchased_item).first()
        if purc_item_object:  # If the object is not None
            if current_user.can_purchase(purc_item_object):
                purc_item_object.assign_ownership(current_user)
                flash(
                    f"Congratulations, you purchased {purc_item_object.name} for ${purc_item_object.price}", category='success')
            else:
                flash(
                    f"You do not have enough money to purchase {purc_item_object.name}", category='danger')
        # ---- End of Purchase Item Logic -------------------------------------------------------

        # --- Start of Sell item logic ----------------------------------------------------------
        # Este es el nombre que conseguimos del form
        sold_item = request.form.get('sold_item')
        # Este es un item de la base de datos
        print(f"Looking for item: {sold_item}")
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        print(f"got {sold_item_object}")
        if sold_item_object:  # If the object is not None
            print("The object is not None")
            if current_user.can_sell(sold_item_object):
                print("The user can sell the item")
                sold_item_object.sell(current_user)
                flash(
                    f"Congratulations, you sold {sold_item_object.name} for ${sold_item_object.price}!", category="success")
            else:
                flash(
                    f"Something went wrong with selling {sold_item_object.name}", category='danger')
        # --- End of Sell item logic --------------------------------------------------------------
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password_1.data)  # i think this calls the @property password and the setter in models.py
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created succesfully, you are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error, with creating an user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()  # Consigo mi form de forms.py
    if form.validate_on_submit():  # validate_on_submit validates that all the info is valid
        # Verify if the users exists
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        # Get the user that is equal to the username in the form
        # AND if the user exists, verify that the password is correct
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # Se loggea al usuario usando el modulo flask_login
            login_user(attempted_user)
            flash(
                f"Hello {attempted_user.username}! You are logged in!", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password do not match. Please try again',
                  category='danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout_page():
    logout_user()  # Esto es parte de flask_login, funciona porque declare en __init__.py que se use flask_login
    flash("Successfully logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/add_item/', methods=['GET', 'POST'])
@login_required
def add_item_page():
    form = AddItemForm()
    if form.validate_on_submit():
        item_to_create = Item(name=form.name.data,
                              price=form.price.data,
                              description=form.description.data,
                              barcode = form.barcode.data)
        db.session.add(item_to_create)
        db.session.commit()
        flash(
            f"Item {item_to_create.name} created succesfully!", category='success')
        return redirect(url_for('add_item_page'))
    if form.errors != {}:  # If there are errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error, with creating an item: {err_msg}', category='danger')
    return render_template('add_item.html', form=form)
