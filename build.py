import os
import shutil
import subprocess

def clean_build():
    """Clean up build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    print("Cleaned build directories")

def build_exe():
    """Build the executable using PyInstaller"""
    try:
        # Clean previous builds
        clean_build()
        
        # Run PyInstaller
        subprocess.run(['pyinstaller', 'AccountingPro.spec'], check=True)
        
        # Copy the database file if it exists
        if os.path.exists('accounting.db'):
            shutil.copy2('accounting.db', 'dist/accounting.db')
        
        print("\nBuild completed successfully!")
        print("Your executable is in the 'dist' folder")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    build_exe()
