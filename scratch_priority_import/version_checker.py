"""
Semantic Version Checker for All-Skills.
Parses, validates, and compares semantic version strings and dependency version ranges.
"""

import re
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)


class SemanticVersion:
    """Represents a Semantic Version (MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD])."""

    _REGEX = re.compile(
        r"^v?(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:\.(?P<patch>\d+))?"
        r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
        r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
    )

    def __init__(self, version_str: str):
        self.raw = version_str.strip()
        match = self._REGEX.match(self.raw)
        if not match:
            # Fallback for simple numeric or non-standard strings
            parts = re.findall(r"\d+", self.raw)
            self.major = int(parts[0]) if parts else 1
            self.minor = int(parts[1]) if len(parts) > 1 else 0
            self.patch = int(parts[2]) if len(parts) > 2 else 0
            self.prerelease = ""
            self.build = ""
        else:
            self.major = int(match.group("major") or 0)
            self.minor = int(match.group("minor") or 0)
            self.patch = int(match.group("patch") or 0)
            self.prerelease = match.group("prerelease") or ""
            self.build = match.group("build") or ""

    @property
    def tuple(self) -> Tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            other = SemanticVersion(other)
        if isinstance(other, SemanticVersion):
            return self.tuple == other.tuple
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, str):
            other = SemanticVersion(other)
        if isinstance(other, SemanticVersion):
            return self.tuple < other.tuple
        return False

    def __le__(self, other: object) -> bool:
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        return not (self <= other)

    def __ge__(self, other: object) -> bool:
        return not (self < other)

    def __str__(self) -> str:
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            s += f"-{self.prerelease}"
        return s


class VersionChecker:
    """Evaluates version specifications and validates compatibility."""

    @staticmethod
    def satisfies(version_str: str, constraint: str) -> bool:
        """
        Check if version satisfies a constraint such as:
        '>=1.0.0', '<2.0.0', '==1.2.3', '^1.2.0', '~1.2.0', '*'
        """
        constraint = constraint.strip()
        if not constraint or constraint == "*":
            return True

        v = SemanticVersion(version_str)

        # Handle compound constraints separated by comma: '>=1.0.0, <2.0.0'
        if "," in constraint:
            sub_constraints = [c.strip() for c in constraint.split(",")]
            return all(VersionChecker.satisfies(version_str, sub) for sub in sub_constraints)

        # Operators
        if constraint.startswith(">="):
            target = SemanticVersion(constraint[2:].strip())
            return v >= target
        elif constraint.startswith("<="):
            target = SemanticVersion(constraint[2:].strip())
            return v <= target
        elif constraint.startswith(">"):
            target = SemanticVersion(constraint[1:].strip())
            return v > target
        elif constraint.startswith("<"):
            target = SemanticVersion(constraint[1:].strip())
            return v < target
        elif constraint.startswith("=="):
            target = SemanticVersion(constraint[2:].strip())
            return v == target
        elif constraint.startswith("^"):  # Compatible within same major
            target = SemanticVersion(constraint[1:].strip())
            if v.major != target.major:
                return False
            return v >= target
        elif constraint.startswith("~"):  # Compatible within same minor
            target = SemanticVersion(constraint[1:].strip())
            if v.major != target.major or v.minor != target.minor:
                return False
            return v >= target
        else:
            target = SemanticVersion(constraint)
            return v == target

    @classmethod
    def check_compatibility(cls, skill_name: str, current_version: str, required_range: str) -> bool:
        """Log and evaluate version satisfaction."""
        satisfied = cls.satisfies(current_version, required_range)
        if not satisfied:
            logger.warning(
                f"Skill '{skill_name}' version {current_version} does not meet constraint '{required_range}'"
            )
        return satisfied
