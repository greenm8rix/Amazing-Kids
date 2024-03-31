from flask_login import UserMixin
from sqlalchemy import ForeignKey
from config import db, app


class LoginModel(db.Model, UserMixin):
    __tablename__ = "user_data"
    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    password = db.Column(db.String(80), nullable=False)
    subscription_tier = db.Column(db.BOOLEAN(), nullable=True)


class StripeCustomer(db.Model):
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(40), db.ForeignKey("user_data.id"))
    stripeCustomerId = db.Column(db.String(255), nullable=False)
    stripeSubscriptionId = db.Column(db.String(255), nullable=False)


class products(db.Model):
    price_id = db.Column(db.String(40), primary_key=True)
    Product = db.Column(db.String(40), nullable=True)


with app.app_context():
    db.create_all()
