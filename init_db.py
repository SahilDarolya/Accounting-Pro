from app import app, db
from models import User, Party, Item, Invoice, Transaction, Inventory, Order, Replacement, Ledger
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@accountingpro.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
