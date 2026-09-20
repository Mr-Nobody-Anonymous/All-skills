"""
Skill-Barcode-Scanner Skill Package.
"""

from .skill import BarcodeScannerSkill

def create_skill():
    return BarcodeScannerSkill()

__all__ = ["BarcodeScannerSkill", "create_skill"]
