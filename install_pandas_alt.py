import subprocess
import sys

def install_with_alternative_method():
    packages = [
        "numpy",
        "pandas"  
    ]
    
    for package in packages:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--index-url", "https://pypi.org/simple",
                "--trusted-host", "pypi.org",
                "--trusted-host", "files.pythonhosted.org",
                "--no-cache-dir",
                "--only-binary", ":all:",  
                package
            ])
            print(f"Successfully installed {package}")
        except Exception as e:
            print(f"Error installing {package}: {str(e)}")
            try:
                # Try alternative installation method
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "--no-deps",
                    "--no-cache-dir",
                    package
                ])
                print(f"Successfully installed {package} using alternative method")
            except Exception as e2:
                print(f"Failed to install {package} using alternative method: {str(e2)}")

if __name__ == "__main__":
    print("Starting alternative installation process...")
    install_with_alternative_method()
    print("\nInstallation process completed!")
