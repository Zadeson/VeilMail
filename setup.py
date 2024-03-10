from setuptools import setup

setup(
    name='FlashMail',
    version='1.0.0',
    py_modules=['flashmail'],
    install_requires=[
        'requests',
        'rich',
        'pyfiglet',
        'yaspin',
        'alive-progress',
        'pyperclip',
        'questionary',
        'html2text'
    ],
    entry_points='''
        [console_scripts]
        flashmail=flashmail:main
    ''',
    author='Ethen Dixon',
    author_email='ethendixon@outlook.com',
    description='A simple command-line email client using the 1secmail API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zadeson/flashmail',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
