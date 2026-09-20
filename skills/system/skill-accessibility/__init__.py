"""
Skill-Accessibility Skill Package.
"""

from .skill import AccessibilitySkill

def create_skill():
    return AccessibilitySkill()

__all__ = ["AccessibilitySkill", "create_skill"]
