from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.String(10), nullable=False)  # Ej. "bitcoin", "ethereum"
    last_price = db.Column(db.Float, nullable=True)
    last_check = db.Column(db.DateTime, nullable=True)

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)