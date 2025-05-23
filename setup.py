"""Setup script for PyKeyEmu package

This script allows PyKeyEmu to be installed as a standard Python package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from __init__.py
version = {}
with open(os.path.join(here, 'pykeyemu', '__init__.py')) as f:
    exec(f.read(), version)

setup(
    name='pykeyemu',
    version='1.0.0',
    description='Python Key Input Emulation Module for Windows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='OutlawRGB',
    author_email='github.shifty771@passinbox.com',
    url='https://github.com/RGB-Outl4w/pykeyemu',
    
    # Package information
    packages=find_packages(),
    python_requires='>=3.8',
    
    # Classification
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Desktop Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    
    # Keywords
    keywords='keyboard input simulation automation windows sendkey keypress',
    
    # Dependencies
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    
    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=0.5',
        ],
    },
    
    # Entry points
    entry_points={
        'console_scripts': [
            'pykeyemu-test=pykeyemu.test_pykeyemu:run_tests',
        ],
    },
    
    # Include additional files
    include_package_data=True,
    package_data={
        'pykeyemu': ['*.md', '*.txt'],
    },
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/RGB-Outl4w/pykeyemu/issues',
        'Source': 'https://github.com/RGB-Outl4w/pykeyemu',
    },
)