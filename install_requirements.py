import subprocess
import sys
import os

def run_pip_command(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        return False

def install_packages():
    # First, upgrade pip itself
    print("Upgrading pip...")
    run_pip_command("python -m pip install --upgrade pip --no-cache-dir")

    packages = [
        "flask==2.3.3",
        "flask-sqlalchemy==3.1.1",
        "flask-login==0.6.2",
        "flask-wtf==1.1.1",
        "sqlalchemy==2.0.20",
        "werkzeug==2.3.7",
        "python-dotenv==1.0.0",
        "flask-migrate==4.0.4",
        "wtforms==3.0.1",
        "pymysql==1.1.0",
        "pandas"
    ]

    print("\nInstalling packages...")
    for package in packages:
        print(f"\nInstalling {package}...")
        cmd = f"pip install {package} --no-cache-dir"
        if run_pip_command(cmd):
            print(f"Successfully installed {package}")
        else:
            print(f"Failed to install {package}, trying alternative method...")
            alt_cmd = f"python -m pip install {package} --no-cache-dir"
            if run_pip_command(alt_cmd):
                print(f"Successfully installed {package} using alternative method")
            else:
                print(f"Failed to install {package}")

if __name__ == "__main__":
    print("Starting installation process...")
    install_packages()
    print("\nInstallation process completed!")
