from setuptools import setup

setup(
    name='VeilMail',
    version='1.0.8',
    packages=find_packages(),
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
    entry_points={
        'console_scripts': [
            'veilmail=veilmail.main:main',
        ],
    },
    author='Ethen Dixon',
    author_email='ethendixon@outlook.com',
    description='A simple command-line email client using the 1secmail API.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zadeson/veilmail',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
