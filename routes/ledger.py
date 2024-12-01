from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import db, Ledger, Party
from datetime import datetime

bp = Blueprint('ledger', __name__)

@bp.route('/ledger')
@login_required
def index():
    parties = Party.query.all()
    return render_template('ledger/index.html', parties=parties)

@bp.route('/ledger/party/<int:party_id>')
@login_required
def party_ledger(party_id):
    party = Party.query.get_or_404(party_id)
    
    # Get date range from request
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    
    query = Ledger.query.filter_by(party_id=party_id)
    
    if start_date:
        query = query.filter(Ledger.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Ledger.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    entries = query.order_by(Ledger.date).all()
    
    return render_template('ledger/party.html', 
                         party=party, 
                         entries=entries)

@bp.route('/api/ledger/summary')
@login_required
def ledger_summary():
    party_id = request.args.get('party_id', type=int)
    
    if not party_id:
        return jsonify({'error': 'Party ID is required'}), 400
    
    # Get latest ledger entry for the party
    latest_entry = Ledger.query.filter_by(party_id=party_id)\
        .order_by(Ledger.id.desc()).first()
    
    if not latest_entry:
        return jsonify({
            'cash_balance': 0,
            'bill_balance': 0,
            'total_balance': 0
        })
    
    return jsonify({
        'cash_balance': latest_entry.cash_balance,
        'bill_balance': latest_entry.bill_balance,
        'total_balance': latest_entry.total_balance
    })

@bp.route('/api/ledger/transactions')
@login_required
def ledger_transactions():
    party_id = request.args.get('party_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Ledger.query.filter_by(party_id=party_id)
    
    if start_date:
        query = query.filter(Ledger.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Ledger.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    entries = query.order_by(Ledger.date).all()
    
    return jsonify([{
        'id': entry.id,
        'date': entry.date.strftime('%Y-%m-%d'),
        'description': entry.description,
        'cash_debit': entry.cash_debit,
        'cash_credit': entry.cash_credit,
        'bill_debit': entry.bill_debit,
        'bill_credit': entry.bill_credit,
        'cash_balance': entry.cash_balance,
        'bill_balance': entry.bill_balance,
        'total_balance': entry.total_balance
    } for entry in entries])
