"""
Skill-Bluetooth Skill Package.
"""

from .skill import BluetoothSkill

def create_skill():
    return BluetoothSkill()

__all__ = ["BluetoothSkill", "create_skill"]
