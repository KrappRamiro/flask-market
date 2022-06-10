from email.policy import default
from market import db
from market import bcrypt


class User(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        print("Creating a password the unsafe way: via plain text :(")
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        print(f"Hasheando contraseña {plain_text_password} con el resultado {self.password_hash}")

class Item(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(length=60), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=60), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'
