from email.policy import default
from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

# I need the is_authenticated, is_active, and is_anonymous methods from login_manager,
# and i know a Class that already has that methods, so lets inherit from that class

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) > 4:
            return f"${self.budget // 1000}K"
        elif len(str(self.budget)) > 7:
            return f"${self.budget // 1000000}M"
        else:
            return f"${self.budget}"

    @property
    def password(self):
        print("Creating a password the unsafe way: via plain text :(")
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        print(f"Hasheando contraseña {plain_text_password} con el resultado {self.password_hash}")
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password) #Returns true or false

class Item(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=60), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'
