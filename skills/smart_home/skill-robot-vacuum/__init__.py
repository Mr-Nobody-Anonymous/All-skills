"""
Skill-Robot-Vacuum Skill Package.
"""

from .skill import RobotVacuumSkill

def create_skill():
    return RobotVacuumSkill()

__all__ = ["RobotVacuumSkill", "create_skill"]
