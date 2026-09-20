"""
Skill-Google-Fit Skill Package.
"""

from .skill import GoogleFitSkill

def create_skill():
    return GoogleFitSkill()

__all__ = ["GoogleFitSkill", "create_skill"]
