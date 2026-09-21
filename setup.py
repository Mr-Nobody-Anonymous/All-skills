from setuptools import setup, find_packages
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Single source of truth for version
version_file = ROOT / "src" / "skills" / "_version.py"
version_match = re.search(r'^__version__ = ["\']([^"\']+)["\']', version_file.read_text(encoding="utf-8"), re.M)
version = version_match.group(1) if version_match else "3.0.0"

long_desc = ""
readme_path = ROOT / "README.md"
if readme_path.exists():
    long_desc = readme_path.read_text(encoding="utf-8")

setup(
    name="all-skills",
    version=version,
    package_dir={"": "src", "scratch_priority_import": "scratch_priority_import"},
    packages=find_packages(where="src") + ["scratch_priority_import"],
    python_requires=">=3.10",
    install_requires=[
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "click>=8.0.0",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
        "attrs>=23.1.0",
        "networkx>=3.1",
    ],
    extras_require={
        "test": [
            "pytest>=7.0",
            "pytest-cov",
        ],
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
            "all-skills=skills.cli:main",
            "agent-skills=skills.cli:main",
        ],
    },
    author="Mr-Nobody-Anonymous",
    description="Universal AI Agent Skill Operating System & Execution Runtime",
    long_description=long_desc,
    long_description_content_type="text/markdown",
)
