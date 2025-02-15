from setuptools import setup

APP = ['src/pdbar.py']
VERSION = '0.1.0'
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/appicon.png',
    'plist': {
        'CFBundleIdentifier': 'com.jriggles.PDBar',
        'CFBundleShortVersionString': VERSION,
        'LSUIElement': True,  # menu bar app
        'NSHumanReadableCopyright': (
            'Copyright © 2025 John Riggles [sudo_whoami] - MIT License'
        ),
    },
    'packages': ['feedparser', 'rumps',],
}

setup(
    app=APP,
    name='PDBar',
    version=VERSION,
    description="Get today's Pixel Dailies theme and show it in the menu bar",
    author='J. Riggles [sudo_whoami]',
    url='https://github.com/JRiggles/PDBar',
    license='MIT',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
