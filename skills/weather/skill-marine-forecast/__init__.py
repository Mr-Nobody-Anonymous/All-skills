"""
Skill-Marine-Forecast Skill Package.
"""

from .skill import MarineForecastSkill

def create_skill():
    return MarineForecastSkill()

__all__ = ["MarineForecastSkill", "create_skill"]
