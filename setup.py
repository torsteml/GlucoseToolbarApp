from setuptools import setup

APP = ['app.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'requests']
}

setup(
    app=APP,
    name='Glucose',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps', 'requests']
)