from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Ledger, Invoice, Inventory, Party
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get summary data for dashboard
    total_sales = db.session.query(db.func.sum(Invoice.total_cash_amount + Invoice.total_bill_amount))\
        .filter(Invoice.type == 'sales').scalar() or 0
    total_purchases = db.session.query(db.func.sum(Invoice.total_cash_amount + Invoice.total_bill_amount))\
        .filter(Invoice.type == 'purchase').scalar() or 0
    total_parties = Party.query.count()
    
    # Get recent transactions
    recent_invoices = Invoice.query.order_by(Invoice.date.desc()).limit(5).all()
    
    # Get inventory alerts (low stock items)
    low_stock_items = Inventory.query.filter(Inventory.quantity < 10).all()
    
    return render_template('dashboard.html',
                         total_sales=total_sales,
                         total_purchases=total_purchases,
                         total_parties=total_parties,
                         recent_invoices=recent_invoices,
                         low_stock_items=low_stock_items)

@bp.route('/api/dashboard/summary')
@login_required
def dashboard_summary():
    today = datetime.utcnow().date()
    
    # Get today's transactions
    today_sales = db.session.query(db.func.sum(Invoice.total_cash_amount + Invoice.total_bill_amount))\
        .filter(Invoice.type == 'sales')\
        .filter(db.func.date(Invoice.date) == today).scalar() or 0
        
    today_purchases = db.session.query(db.func.sum(Invoice.total_cash_amount + Invoice.total_bill_amount))\
        .filter(Invoice.type == 'purchase')\
        .filter(db.func.date(Invoice.date) == today).scalar() or 0
    
    return jsonify({
        'today_sales': today_sales,
        'today_purchases': today_purchases
    })
