"""
Skill-Bucket-List Skill Package.
"""

from .skill import BucketListSkill

def create_skill():
    return BucketListSkill()

__all__ = ["BucketListSkill", "create_skill"]
