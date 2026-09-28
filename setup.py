"""Compatibility shim for legacy tooling (``python setup.py ...``).

All package metadata, dependencies and the version source are declared in
``pyproject.toml`` (PEP 621). Do not add metadata here: duplicating fields that
the ``[project]`` table does not list as ``dynamic`` makes modern setuptools
reset them, which previously broke ``pip install -e .`` in CI.
"""

from setuptools import setup

setup()
