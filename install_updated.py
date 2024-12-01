import subprocess
import sys
import time

def run_pip_command(command_list):
    try:
        subprocess.check_call(command_list)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        return False

def install_packages():
    base_command = [
        sys.executable, "-m", "pip", "install",
        "--index-url", "https://pypi.org/simple",
        "--trusted-host", "pypi.org",
        "--trusted-host", "files.pythonhosted.org",
        "--no-cache-dir"
    ]

    # Install packages in order
    packages = [
        "Werkzeug>=3.0.1",
        "click>=8.1.7",
        "importlib-metadata>=7.0.1",
        "itsdangerous>=2.1.2",
        "Jinja2>=3.1.3",
        "Flask>=3.0.0",
        "greenlet>=3.0.3",
        "typing_extensions>=4.9.0",
        "SQLAlchemy>=2.0.25",
        "Flask-SQLAlchemy>=3.1.0",
        "Flask-Login>=0.6.3",
        "Flask-WTF>=1.2.1",
        "python-dotenv>=1.0.0",
        "Flask-Migrate>=4.0.5",
        "WTForms>=3.1.1",
        "pymysql>=1.1.0",
        "numpy>=1.26.0",
        "pandas>=2.2.0"
    ]

    print("\nInstalling packages...")
    for package in packages:
        print(f"\nInstalling {package}...")
        if run_pip_command(base_command + [package]):
            print(f"Successfully installed {package}")
        else:
            print(f"Failed to install {package}")
        time.sleep(1)  # Small delay between installations

if __name__ == "__main__":
    print("Starting installation process...")
    install_packages()
    print("\nInstallation process completed!")
