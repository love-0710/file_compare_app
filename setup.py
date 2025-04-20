from setuptools import setup, find_packages
import os
import sys

# Ensure you are using the correct Python version
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    raise Exception("Python 3.6 or above is required.")

# Read the long description from your README file (if you have one)
def read_readme():
    try:
        with open("README.md", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Setup configuration
setup(
    name="SmartComparePro",
    version="1.0.0",
    author="Love Kumar Yadav",
    author_email="ylovekumar@statestreet.com",
    description="A smart file comparison tool similar to Beyond Compare, with advanced features.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://www.linkedin.com/in/love-yadav-191621276/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Allow the app to run on any OS
    ],
    install_requires=[
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "openpyxl>=3.0.7",  # For Excel support
        "fuzzywuzzy>=0.18.0",  # For fuzzy matching
        "pyinstaller>=4.5.1",  # PyInstaller to create the EXE
        # Add any other dependencies you require
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "smartcomparepro = main:main",  # Entry point for running the app
        ]
    },
    include_package_data=True,  # Include additional non-Python files, if needed (like images, configuration files, etc.)
)
