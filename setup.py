#!/usr/bin/env python3
"""
Setup script for Hotel Booking System
Integrates with Maven build process
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    elif os.path.exists("Readme.txt"):
        with open("Readme.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "Hotel Booking System"

# Read requirements
def read_requirements():
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="hotel-booking-system",
    version="1.0.0",
    description="A Python hotel booking system with Maven integration",
    long_description=read_readme(),
    long_description_content_type="text/plain",
    author="Hotel Booking Team",
    author_email="team@hotelbooking.com",
    url="https://github.com/kevgum/assignment2",
    py_modules=["hotel"],
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "hotel-booking=hotel:main",
        ],
    },
)
