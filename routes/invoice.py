from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from models import db, Invoice, Transaction, Item, Party, Ledger
from datetime import datetime

bp = Blueprint('invoice', __name__)

@bp.route('/invoice/new', methods=['GET', 'POST'])
@login_required
def new_invoice():
    if request.method == 'POST':
        data = request.json
        
        # Create new invoice
        invoice = Invoice(
            invoice_number=data['invoice_number'],
            party_id=data['party_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            type=data['type'],
            total_cash_amount=data['total_cash_amount'],
            total_bill_amount=data['total_bill_amount']
        )
        db.session.add(invoice)
        db.session.flush()
        
        # Add transactions
        for item in data['items']:
            transaction = Transaction(
                invoice_id=invoice.id,
                item_id=item['item_id'],
                quantity=item['quantity'],
                cash_rate=item['cash_rate'],
                bill_rate=item['bill_rate'],
                cash_amount=item['cash_amount'],
                bill_amount=item['bill_amount']
            )
            db.session.add(transaction)
            
            # Update inventory
            update_inventory(item['item_id'], item['quantity'], data['type'])
        
        # Create ledger entry
        create_ledger_entry(invoice)
        
        db.session.commit()
        return jsonify({'status': 'success', 'invoice_id': invoice.id})
        
    parties = Party.query.all()
    items = Item.query.all()
    return render_template('invoice/new.html', parties=parties, items=items)

@bp.route('/invoice/<int:id>')
@login_required
def view_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    transactions = Transaction.query.filter_by(invoice_id=id).all()
    return render_template('invoice/view.html', invoice=invoice, transactions=transactions)

@bp.route('/invoice/list')
@login_required
def list_invoices():
    invoices = Invoice.query.order_by(Invoice.date.desc()).all()
    return render_template('invoice/list.html', invoices=invoices)

def update_inventory(item_id, quantity, invoice_type):
    from models import Inventory
    inventory = Inventory.query.filter_by(item_id=item_id).first()
    
    if not inventory:
        inventory = Inventory(item_id=item_id, quantity=0)
        db.session.add(inventory)
    
    if invoice_type == 'purchase':
        inventory.quantity += quantity
    else:  # sales
        inventory.quantity -= quantity
    
    inventory.last_updated = datetime.utcnow()

def create_ledger_entry(invoice):
    ledger = Ledger(
        date=invoice.date,
        party_id=invoice.party_id,
        invoice_id=invoice.id,
        description=f"{'Sales' if invoice.type == 'sales' else 'Purchase'} Invoice #{invoice.invoice_number}"
    )
    
    if invoice.type == 'sales':
        ledger.cash_debit = invoice.total_cash_amount
        ledger.bill_debit = invoice.total_bill_amount
    else:  # purchase
        ledger.cash_credit = invoice.total_cash_amount
        ledger.bill_credit = invoice.total_bill_amount
    
    # Calculate running balances
    last_entry = Ledger.query.filter_by(party_id=invoice.party_id)\
        .order_by(Ledger.id.desc()).first()
    
    if last_entry:
        ledger.cash_balance = last_entry.cash_balance
        ledger.bill_balance = last_entry.bill_balance
    else:
        ledger.cash_balance = 0
        ledger.bill_balance = 0
    
    if invoice.type == 'sales':
        ledger.cash_balance += invoice.total_cash_amount
        ledger.bill_balance += invoice.total_bill_amount
    else:
        ledger.cash_balance -= invoice.total_cash_amount
        ledger.bill_balance -= invoice.total_bill_amount
    
    ledger.total_balance = ledger.cash_balance + ledger.bill_balance
    db.session.add(ledger)
