from app import app, db
from app.models import Subscription
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def check_prices():
    with app.app_context():
        subscriptions = Subscription.query.all()
        for sub in subscriptions:
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={sub.crypto_id}&vs_currencies=usd")
            price = response.json()[sub.crypto_id]['usd']
            if sub.last_price and sub.last_check:
                if (datetime.datetime.utcnow() - sub.last_check).total_seconds() > 24*3600:
                    variation = ((price - sub.last_price) / sub.last_price) * 100
                    if abs(variation) > 5:  # Notificar si varía más del 5%
                        print(f"Notificación para {sub.user_id}: {sub.crypto_id} varió {variation}%")
                        # Aquí integra un servicio de notificación (email, SMS, etc.)
            sub.last_price = price
            sub.last_check = datetime.datetime.utcnow()
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(check_prices, 'interval', hours=1)
scheduler.start()