"""
Skill-Llama Skill Package.
"""

from .skill import LlamaSkill

def create_skill():
    return LlamaSkill()

__all__ = ["LlamaSkill", "create_skill"]
