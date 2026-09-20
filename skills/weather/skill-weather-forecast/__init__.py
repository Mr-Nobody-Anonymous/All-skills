"""
Skill-Weather-Forecast Skill Package.
"""

from .skill import WeatherForecastSkill

def create_skill():
    return WeatherForecastSkill()

__all__ = ["WeatherForecastSkill", "create_skill"]
