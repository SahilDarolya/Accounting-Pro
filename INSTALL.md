# AccountingPro Installation Guide

## System Requirements
- Windows 7/8/10/11
- 4GB RAM (minimum)
- 500MB free disk space
- Internet connection (for initial setup)

## Installation Steps

### For Users (Installing the Software)
1. Download the AccountingPro installer
2. Run the installer (AccountingPro_Setup.exe)
3. Follow the installation wizard
4. Launch AccountingPro from desktop shortcut or start menu

### For Developers (Building the Installer)

1. Install required build dependencies:
```bash
pip install cx_Freeze
pip install -r requirements.txt
```

2. Build the executable:
```bash
python setup.py build
```

3. Create the installer:
```bash
python setup.py bdist_msi
```

The installer will be created in the `dist` directory.

## First Time Setup
1. Launch AccountingPro
2. Create admin account when prompted
3. Configure company details
4. Start using the software!

## Troubleshooting
- If the application doesn't start, check if port 5000 is available
- For database issues, try restarting the application
- Contact support at support@accountingpro.com

## Uninstallation
1. Go to Control Panel > Programs and Features
2. Find AccountingPro and click Uninstall
3. Follow the uninstallation wizard
