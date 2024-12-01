import os
import sys
import webbrowser
import threading
import time
from app import app
import socket
import qrcode
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from pyngrok import ngrok

def create_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "access_qr.png")
    qr_image.save(qr_path)
    return qr_path

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def open_browser(public_url):
    # Wait a bit for the server to start
    time.sleep(1.5)
    print(f"\nAccess your application:")
    print(f"1. Public URL: {public_url}")
    print(f"2. QR Code has been generated as 'access_qr.png'")
    print("\nYou can access this URL from any device with internet connection!")
    
    # Generate QR code
    qr_path = create_qr_code(public_url)
    print(f"3. Scan the QR code in {qr_path} with your mobile device to access the app\n")
    
    # Open in default browser
    webbrowser.open(public_url)

def run_app():
    if getattr(sys, 'frozen', False):
        # If we're running as a PyInstaller bundle
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app.template_folder = template_folder
        app.static_folder = static_folder
    
    # Add security measures
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Force HTTPS in production
    if not app.debug:
        Talisman(app)
    
    # Get port and start ngrok
    port = find_free_port()
    public_url = ngrok.connect(port).public_url
    
    # Start browser in a new thread
    threading.Thread(target=open_browser, args=(public_url,), daemon=True).start()
    
    # Start Flask app
    app.run(port=port, debug=False)

if __name__ == '__main__':
    run_app()
