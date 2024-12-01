# Full-Fledged Accounting Software

A comprehensive accounting software solution with advanced features for business management.

## Features

- **Dashboard**: Overview of key financial metrics and activities
- **Invoice Management**: 
  - Dual pricing system (Cash + Bill)
  - Automatic ledger updates
  - Transaction tracking
- **Order Management**
- **Sales & Purchase Tracking**
- **Party Management**
- **Inventory Management**
- **Advanced Ledger System**:
  - Cash Credit/Debit tracking
  - Bill Credit/Debit tracking
  - Running balances (Cash, Bill, Total)
- **Replacement Management**
- **Reports Generation**

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```
   flask run
   ```

## Database Structure

The application uses SQLAlchemy with the following main tables:
- Parties
- Items
- Invoices
- Transactions
- Inventory
- Orders
- Replacements
- Ledger
