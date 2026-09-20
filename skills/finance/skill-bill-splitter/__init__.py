"""
Skill-Bill-Splitter Skill Package.
"""

from .skill import BillSplitterSkill

def create_skill():
    return BillSplitterSkill()

__all__ = ["BillSplitterSkill", "create_skill"]
