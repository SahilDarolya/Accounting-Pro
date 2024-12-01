from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Item, Inventory, Transaction
from sqlalchemy import func

bp = Blueprint('inventory', __name__)

@bp.route('/inventory')
@login_required
def index():
    items = db.session.query(
        Item,
        Inventory.quantity,
        func.sum(Transaction.quantity).label('total_sold')
    ).join(
        Inventory,
        Item.id == Inventory.item_id
    ).outerjoin(
        Transaction,
        Item.id == Transaction.item_id
    ).group_by(Item.id).all()
    
    return render_template('inventory/index.html', items=items)

@bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        data = request.json
        
        item = Item(
            name=data['name'],
            description=data['description'],
            cash_rate=data['cash_rate'],
            bill_rate=data['bill_rate'],
            unit=data['unit']
        )
        db.session.add(item)
        db.session.flush()
        
        inventory = Inventory(
            item_id=item.id,
            quantity=data['initial_quantity']
        )
        db.session.add(inventory)
        
        try:
            db.session.commit()
            return jsonify({'status': 'success', 'item_id': item.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
            
    return render_template('inventory/add.html')

@bp.route('/inventory/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    inventory = Inventory.query.filter_by(item_id=id).first()
    
    if request.method == 'POST':
        data = request.json
        
        item.name = data['name']
        item.description = data['description']
        item.cash_rate = data['cash_rate']
        item.bill_rate = data['bill_rate']
        item.unit = data['unit']
        
        if 'quantity_adjustment' in data:
            inventory.quantity += float(data['quantity_adjustment'])
        
        try:
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
            
    return render_template('inventory/edit.html', item=item, inventory=inventory)

@bp.route('/api/inventory/stock-alert')
@login_required
def stock_alert():
    low_stock_items = db.session.query(
        Item,
        Inventory.quantity
    ).join(
        Inventory,
        Item.id == Inventory.item_id
    ).filter(
        Inventory.quantity < 10
    ).all()
    
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'quantity': quantity,
        'unit': item.unit
    } for item, quantity in low_stock_items])

@bp.route('/api/inventory/movement/<int:id>')
@login_required
def item_movement(id):
    transactions = Transaction.query.filter_by(item_id=id)\
        .order_by(Transaction.created_at.desc())\
        .limit(10).all()
        
    return jsonify([{
        'date': t.created_at.strftime('%Y-%m-%d'),
        'quantity': t.quantity,
        'type': 'Sale' if t.invoice.type == 'sales' else 'Purchase',
        'invoice_number': t.invoice.invoice_number
    } for t in transactions])
