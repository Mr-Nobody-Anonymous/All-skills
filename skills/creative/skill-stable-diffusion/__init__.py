"""
Skill-Stable-Diffusion Skill Package.
"""

from .skill import StableDiffusionSkill

def create_skill():
    return StableDiffusionSkill()

__all__ = ["StableDiffusionSkill", "create_skill"]
