from setuptools import setup, find_packages
import os

long_desc = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_desc = f.read()

setup(
    name="all-skills",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov",
            "black",
            "ruff",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "all-skills=scratch_priority_import.cli:main",
        ],
    },
    author="Mr-Nobody-Anonymous",
    description="Universal skill catalog and dependency management system",
    long_description=long_desc,
    long_description_content_type="text/markdown",
)
