from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, db
from app.models import User, Subscription
import requests
import datetime

# Registro de usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], password=data['password'])  # Hash password en producción
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:  # Validar password en producción
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Suscribirse a una criptomoneda
@app.route('/subscribe/<crypto_id>', methods=['POST'])
@jwt_required()
def subscribe(crypto_id):
    user_id = get_jwt_identity()
    subscription = Subscription(user_id=user_id, crypto_id=crypto_id)
    db.session.add(subscription)
    db.session.commit()
    return jsonify({"message": f"Subscribed to {crypto_id}"}), 200

# Obtener precios y variaciones
@app.route('/prices', methods=['GET'])
@jwt_required()
def get_prices():
    user_id = get_jwt_identity()
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    prices = {}
    for sub in subscriptions:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={sub.crypto_id}&vs_currencies=usd")
        price = response.json()[sub.crypto_id]['usd']
        prices[sub.crypto_id] = {"current_price": price}
        if sub.last_price and sub.last_check:
            variation = ((price - sub.last_price) / sub.last_price) * 100
            prices[sub.crypto_id]["variation_24h"] = variation
        sub.last_price = price
        sub.last_check = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(prices), 200