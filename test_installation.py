def test_imports():
    packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'sqlalchemy',
        'werkzeug',
        'dotenv',
        'flask_migrate',
        'wtforms',
        'pymysql'
    ]

    print("Testing package imports...")
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} successfully imported")
        except ImportError as e:
            print(f"✗ {package} import failed: {str(e)}")

    # Test pandas separately since it might not be installed yet
    try:
        import pandas
        print("✓ pandas successfully imported")
    except ImportError as e:
        print(f"✗ pandas import failed: {str(e)}")

if __name__ == "__main__":
    test_imports()
