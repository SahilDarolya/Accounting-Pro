import subprocess
import os

def install_wheel(wheel_path):
    try:
        subprocess.check_call(['pip', 'install', wheel_path])
        print(f"Successfully installed {os.path.basename(wheel_path)}")
    except Exception as e:
        print(f"Error installing {os.path.basename(wheel_path)}: {str(e)}")

wheels_dir = "wheels"
wheels = [
    "numpy‑2.1.3‑cp313‑cp313‑win_amd64.whl",
    "pandas‑2.2.3‑cp313‑cp313‑win_amd64.whl"
]

print("Installing wheels...")
for wheel in wheels:
    wheel_path = os.path.join(wheels_dir, wheel)
    if os.path.exists(wheel_path):
        install_wheel(wheel_path)
    else:
        print(f"Wheel file not found: {wheel}")

print("Installation complete!")
