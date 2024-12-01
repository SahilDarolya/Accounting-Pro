from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import models
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import remaining models and routes
from models import Party, Item, Invoice, Transaction, Inventory, Order, Replacement, Ledger
from routes import main, auth, invoice, inventory, ledger, party, order, reports

# Register blueprints
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(invoice.bp)
app.register_blueprint(inventory.bp)
app.register_blueprint(ledger.bp)
app.register_blueprint(party.bp)
app.register_blueprint(order.bp)
app.register_blueprint(reports.bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
