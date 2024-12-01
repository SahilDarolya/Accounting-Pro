import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "flask",
        "sqlalchemy",
        "werkzeug",
        "jinja2",
        "flask_sqlalchemy",
        "flask_login",
        "flask_migrate",
        "flask_wtf",
        "pandas",
        "webbrowser"
    ],
    "excludes": [],
    "include_files": [
        ("static", "static"),
        ("templates", "templates"),
        ("README.md", "README.md"),
        ("requirements.txt", "requirements.txt")
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this to hide console window

setup(
    name="AccountingPro",
    version="1.0.0",
    description="Professional Accounting Management System",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "installer_start.py",
            base=base,
            icon="static/img/icon.ico",
            target_name="AccountingPro.exe",
            shortcut_name="AccountingPro",
            shortcut_dir="DesktopFolder"
        )
    ]
)
