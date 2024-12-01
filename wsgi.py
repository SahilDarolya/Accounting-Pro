from app import app as application, db

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run()
