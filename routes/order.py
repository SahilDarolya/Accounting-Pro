from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Order, Party, Item, Invoice, Transaction
from datetime import datetime

bp = Blueprint('order', __name__)

@bp.route('/orders')
@login_required
def index():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('order/index.html', orders=orders)

@bp.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    if request.method == 'POST':
        data = request.json
        
        order = Order(
            order_number=data['order_number'],
            party_id=data['party_id'],
            status='pending',
            total_amount=data['total_amount']
        )
        
        try:
            db.session.add(order)
            db.session.commit()
            
            # If auto-generate invoice is requested
            if data.get('generate_invoice'):
                create_invoice_from_order(order, data['items'])
                
            return jsonify({'status': 'success', 'order_id': order.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    parties = Party.query.all()
    items = Item.query.all()
    return render_template('order/new.html', parties=parties, items=items)

@bp.route('/order/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    return render_template('order/view.html', order=order)

@bp.route('/order/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    order = Order.query.get_or_404(id)
    data = request.json
    
    order.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/order/<int:id>/convert', methods=['POST'])
@login_required
def convert_to_invoice(id):
    order = Order.query.get_or_404(id)
    data = request.json
    
    try:
        invoice = create_invoice_from_order(order, data['items'])
        return jsonify({
            'status': 'success',
            'invoice_id': invoice.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

def create_invoice_from_order(order, items):
    invoice = Invoice(
        invoice_number=f"INV-{order.order_number}",
        party_id=order.party_id,
        date=datetime.utcnow(),
        type='sales',
        total_cash_amount=sum(item['cash_amount'] for item in items),
        total_bill_amount=sum(item['bill_amount'] for item in items),
        status='pending'
    )
    db.session.add(invoice)
    db.session.flush()
    
    for item in items:
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
    
    order.status = 'converted'
    db.session.commit()
    
    return invoice
