from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20))
    address = db.Column(db.Text)
    email = db.Column(db.String(120))
    gst_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cash_rate = db.Column(db.Float, nullable=False)
    bill_rate = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_cash_amount = db.Column(db.Float, default=0)
    total_bill_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    type = db.Column(db.String(20))  # sales/purchase
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Float)
    cash_rate = db.Column(db.Float)
    bill_rate = db.Column(db.Float)
    cash_amount = db.Column(db.Float)
    bill_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    status = db.Column(db.String(20))
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Replacement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Float)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    description = db.Column(db.Text)
    cash_debit = db.Column(db.Float, default=0)
    cash_credit = db.Column(db.Float, default=0)
    bill_debit = db.Column(db.Float, default=0)
    bill_credit = db.Column(db.Float, default=0)
    cash_balance = db.Column(db.Float)
    bill_balance = db.Column(db.Float)
    total_balance = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
