import ssl
import subprocess
import sys

def fix_ssl():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Update pip to latest version with SSL verification disabled
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--trusted-host", "pypi.org",
            "--trusted-host", "files.pythonhosted.org",
            "--upgrade", "pip"
        ])
        print("Successfully upgraded pip")
    except Exception as e:
        print(f"Error upgrading pip: {str(e)}")

if __name__ == "__main__":
    print("Fixing SSL settings...")
    fix_ssl()
    print("SSL fix completed!")
