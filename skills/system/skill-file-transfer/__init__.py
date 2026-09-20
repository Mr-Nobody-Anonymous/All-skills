"""
Skill-File-Transfer Skill Package.
"""

from .skill import FileTransferSkill

def create_skill():
    return FileTransferSkill()

__all__ = ["FileTransferSkill", "create_skill"]
