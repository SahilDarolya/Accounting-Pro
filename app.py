from flask import Flask, render_template, redirect, url_for
import os

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

    # Database configuration
    if os.environ.get('RENDER'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///accounting.db')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    from extensions import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

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

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
