import os
import sys
import webbrowser
import threading
import time
from app import app, db

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)  # Wait for Flask to start
    webbrowser.open('http://localhost:5000')

def main():
    # Create database if it doesn't exist
    with app.app_context():
        db.create_all()
    
    # Start browser in a new thread
    threading.Thread(target=open_browser).start()
    
    # Start Flask application
    app.run(debug=False, use_reloader=False)

if __name__ == '__main__':
    main()
