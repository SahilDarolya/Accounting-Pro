from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Party, Invoice, Ledger
from sqlalchemy import func

bp = Blueprint('party', __name__)

@bp.route('/parties')
@login_required
def index():
    parties = db.session.query(
        Party,
        func.sum(Invoice.total_cash_amount + Invoice.total_bill_amount).label('total_business'),
        func.count(Invoice.id).label('total_invoices')
    ).outerjoin(
        Invoice,
        Party.id == Invoice.party_id
    ).group_by(Party.id).all()
    
    return render_template('party/index.html', parties=parties)

@bp.route('/party/add', methods=['GET', 'POST'])
@login_required
def add_party():
    if request.method == 'POST':
        data = request.json
        
        party = Party(
            name=data['name'],
            contact=data['contact'],
            address=data['address'],
            email=data['email'],
            gst_number=data['gst_number']
        )
        
        try:
            db.session.add(party)
            db.session.commit()
            return jsonify({'status': 'success', 'party_id': party.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
            
    return render_template('party/add.html')

@bp.route('/party/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_party(id):
    party = Party.query.get_or_404(id)
    
    if request.method == 'POST':
        data = request.json
        
        party.name = data['name']
        party.contact = data['contact']
        party.address = data['address']
        party.email = data['email']
        party.gst_number = data['gst_number']
        
        try:
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
            
    return render_template('party/edit.html', party=party)

@bp.route('/api/party/<int:id>/summary')
@login_required
def party_summary(id):
    # Get latest ledger entry
    latest_ledger = Ledger.query.filter_by(party_id=id)\
        .order_by(Ledger.id.desc()).first()
    
    # Get transaction summary
    summary = db.session.query(
        func.count(Invoice.id).label('total_invoices'),
        func.sum(case([(Invoice.type == 'sales', Invoice.total_cash_amount + Invoice.total_bill_amount)])).label('total_sales'),
        func.sum(case([(Invoice.type == 'purchase', Invoice.total_cash_amount + Invoice.total_bill_amount)])).label('total_purchases')
    ).filter(
        Invoice.party_id == id
    ).first()
    
    return jsonify({
        'cash_balance': latest_ledger.cash_balance if latest_ledger else 0,
        'bill_balance': latest_ledger.bill_balance if latest_ledger else 0,
        'total_balance': latest_ledger.total_balance if latest_ledger else 0,
        'total_invoices': summary.total_invoices or 0,
        'total_sales': float(summary.total_sales or 0),
        'total_purchases': float(summary.total_purchases or 0)
    })

@bp.route('/api/party/<int:id>/transactions')
@login_required
def party_transactions(id):
    invoices = Invoice.query.filter_by(party_id=id)\
        .order_by(Invoice.date.desc())\
        .limit(10).all()
        
    return jsonify([{
        'date': invoice.date.strftime('%Y-%m-%d'),
        'invoice_number': invoice.invoice_number,
        'type': invoice.type,
        'total_amount': invoice.total_cash_amount + invoice.total_bill_amount
    } for invoice in invoices])
