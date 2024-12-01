from flask import Blueprint, render_template, send_file, request
from flask_login import login_required
from models import db, Invoice, Transaction, Party, Item, Ledger
import pandas as pd
from datetime import datetime
import os
from sqlalchemy import func
import tempfile

bp = Blueprint('reports', __name__)

@bp.route('/reports')
@login_required
def index():
    parties = Party.query.order_by(Party.name).all()
    return render_template('reports/index.html', parties=parties)

@bp.route('/reports/sales')
@login_required
def export_sales():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        Invoice.invoice_number,
        Invoice.date,
        Party.name.label('party_name'),
        Invoice.total_cash_amount,
        Invoice.total_bill_amount,
        Invoice.status
    ).join(Party).filter(Invoice.type == 'sales')
    
    if start_date:
        query = query.filter(Invoice.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Invoice.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    sales = query.all()
    
    df = pd.DataFrame([{
        'Invoice Number': s.invoice_number,
        'Date': s.date.strftime('%Y-%m-%d'),
        'Party Name': s.party_name,
        'Cash Amount': s.total_cash_amount,
        'Bill Amount': s.total_bill_amount,
        'Total Amount': s.total_cash_amount + s.total_bill_amount,
        'Status': s.status
    } for s in sales])
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False, sheet_name='Sales Report')
        tmp_path = tmp.name
    
    return send_file(
        tmp_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'sales_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )

@bp.route('/reports/inventory')
@login_required
def export_inventory():
    query = db.session.query(
        Item.name,
        Item.description,
        Item.cash_rate,
        Item.bill_rate,
        Item.unit,
        func.coalesce(func.sum(Transaction.quantity), 0).label('total_transactions'),
        func.coalesce(Inventory.quantity, 0).label('current_stock')
    ).outerjoin(Transaction).outerjoin(Inventory).group_by(Item.id)
    
    inventory = query.all()
    
    df = pd.DataFrame([{
        'Item Name': i.name,
        'Description': i.description,
        'Cash Rate': i.cash_rate,
        'Bill Rate': i.bill_rate,
        'Unit': i.unit,
        'Total Transactions': i.total_transactions,
        'Current Stock': i.current_stock
    } for i in inventory])
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False, sheet_name='Inventory Report')
        tmp_path = tmp.name
    
    return send_file(
        tmp_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'inventory_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )

@bp.route('/reports/ledger')
@login_required
def export_ledger():
    party_id = request.args.get('party_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        Ledger.date,
        Party.name.label('party_name'),
        Ledger.description,
        Ledger.cash_debit,
        Ledger.cash_credit,
        Ledger.bill_debit,
        Ledger.bill_credit,
        Ledger.cash_balance,
        Ledger.bill_balance,
        Ledger.total_balance
    ).join(Party)
    
    if party_id:
        query = query.filter(Ledger.party_id == party_id)
    if start_date:
        query = query.filter(Ledger.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Ledger.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    ledger = query.order_by(Ledger.date).all()
    
    df = pd.DataFrame([{
        'Date': l.date.strftime('%Y-%m-%d'),
        'Party Name': l.party_name,
        'Description': l.description,
        'Cash Debit': l.cash_debit,
        'Cash Credit': l.cash_credit,
        'Bill Debit': l.bill_debit,
        'Bill Credit': l.bill_credit,
        'Cash Balance': l.cash_balance,
        'Bill Balance': l.bill_balance,
        'Total Balance': l.total_balance
    } for l in ledger])
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False, sheet_name='Ledger Report')
        tmp_path = tmp.name
    
    return send_file(
        tmp_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'ledger_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )
