from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80), nullable = True, unique = True)
    password = db.Column(db.String(120), nullable = True, unique = True)
    google_id = db.Column(db.String(120), nullable = True, unique = True)
    email = db.Column(db.String(120), nullable = True, unique = True)
    role = db.Column(db.String(120), default = 'user')

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), default="../frontend/assets/beef.jpg")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')