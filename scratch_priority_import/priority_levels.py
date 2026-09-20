"""
Priority Levels and Tier Definitions for All-Skills.
Defines the 7 standard execution and loading tiers (Tier 0 to Tier 6).
"""

from enum import IntEnum
from typing import Dict, List, Optional, Set


class PriorityTier(IntEnum):
    """Priority tiers ordered from highest precedence (0) to lowest (6)."""
    TIER_0_CRITICAL = 0    # Core system skills (volume, settings, stop, help, fallback)
    TIER_1_ESSENTIAL = 1   # Time, date, weather, alarm, timer
    TIER_2_HIGH = 2        # Calendar, reminders, notes, calculator, media playback
    TIER_3_MEDIUM = 3      # News, smart home, navigation, email
    TIER_4_STANDARD = 4    # Health, finance, education, cooking, shopping
    TIER_5_LOW = 5         # Games, entertainment, fun, creative, social
    TIER_6_LAZY = 6        # Rarely used, loaded on demand (agriculture, legal, automotive diagnostics)

    @classmethod
    def from_name(cls, name: str) -> "PriorityTier":
        """Convert a string name or alias to a PriorityTier."""
        clean = name.strip().upper().replace(" ", "_").replace("-", "_")
        if not clean.startswith("TIER_"):
            clean = f"TIER_{clean}"
        for tier in cls:
            if tier.name == clean or str(tier.value) == name.strip():
                return tier
        # Alias checks
        aliases: Dict[str, PriorityTier] = {
            "CRITICAL": cls.TIER_0_CRITICAL,
            "SYSTEM": cls.TIER_0_CRITICAL,
            "ESSENTIAL": cls.TIER_1_ESSENTIAL,
            "HIGH": cls.TIER_2_HIGH,
            "MEDIUM": cls.TIER_3_MEDIUM,
            "STANDARD": cls.TIER_4_STANDARD,
            "NORMAL": cls.TIER_4_STANDARD,
            "LOW": cls.TIER_5_LOW,
            "FUN": cls.TIER_5_LOW,
            "LAZY": cls.TIER_6_LAZY,
            "ON_DEMAND": cls.TIER_6_LAZY,
        }
        stripped = name.strip().upper()
        if stripped in aliases:
            return aliases[stripped]
        return cls.TIER_4_STANDARD

    @property
    def label(self) -> str:
        """Human-readable tier label."""
        labels = {
            PriorityTier.TIER_0_CRITICAL: "CRITICAL",
            PriorityTier.TIER_1_ESSENTIAL: "ESSENTIAL",
            PriorityTier.TIER_2_HIGH: "HIGH",
            PriorityTier.TIER_3_MEDIUM: "MEDIUM",
            PriorityTier.TIER_4_STANDARD: "STANDARD",
            PriorityTier.TIER_5_LOW: "LOW",
            PriorityTier.TIER_6_LAZY: "LAZY",
        }
        return labels[self]

    @property
    def max_load_time_seconds(self) -> float:
        """Maximum allowable loading latency budget in seconds."""
        budgets = {
            PriorityTier.TIER_0_CRITICAL: 0.25,
            PriorityTier.TIER_1_ESSENTIAL: 0.50,
            PriorityTier.TIER_2_HIGH: 1.0,
            PriorityTier.TIER_3_MEDIUM: 2.5,
            PriorityTier.TIER_4_STANDARD: 5.0,
            PriorityTier.TIER_5_LOW: 10.0,
            PriorityTier.TIER_6_LAZY: 30.0,
        }
        return budgets[self]


# Predefined domain/keyword to tier mapping
DEFAULT_TIER_MAPPING: Dict[str, PriorityTier] = {
    # Tier 0: Critical
    "system": PriorityTier.TIER_0_CRITICAL,
    "volume": PriorityTier.TIER_0_CRITICAL,
    "settings": PriorityTier.TIER_0_CRITICAL,
    "stop": PriorityTier.TIER_0_CRITICAL,
    "help": PriorityTier.TIER_0_CRITICAL,
    "fallback": PriorityTier.TIER_0_CRITICAL,
    "diagnostics": PriorityTier.TIER_0_CRITICAL,

    # Tier 1: Essential
    "time": PriorityTier.TIER_1_ESSENTIAL,
    "date": PriorityTier.TIER_1_ESSENTIAL,
    "weather": PriorityTier.TIER_1_ESSENTIAL,
    "alarm": PriorityTier.TIER_1_ESSENTIAL,
    "timer": PriorityTier.TIER_1_ESSENTIAL,
    "clock": PriorityTier.TIER_1_ESSENTIAL,

    # Tier 2: High
    "calendar": PriorityTier.TIER_2_HIGH,
    "reminders": PriorityTier.TIER_2_HIGH,
    "notes": PriorityTier.TIER_2_HIGH,
    "calculator": PriorityTier.TIER_2_HIGH,
    "media": PriorityTier.TIER_2_HIGH,
    "music": PriorityTier.TIER_2_HIGH,
    "audio": PriorityTier.TIER_2_HIGH,

    # Tier 3: Medium
    "news": PriorityTier.TIER_3_MEDIUM,
    "smart_home": PriorityTier.TIER_3_MEDIUM,
    "home_assistant": PriorityTier.TIER_3_MEDIUM,
    "homeassistant": PriorityTier.TIER_3_MEDIUM,
    "iot": PriorityTier.TIER_3_MEDIUM,
    "navigation": PriorityTier.TIER_3_MEDIUM,

    "traffic": PriorityTier.TIER_3_MEDIUM,
    "email": PriorityTier.TIER_3_MEDIUM,
    "communication": PriorityTier.TIER_3_MEDIUM,
    "messaging": PriorityTier.TIER_3_MEDIUM,

    # Tier 4: Standard
    "health": PriorityTier.TIER_4_STANDARD,
    "fitness": PriorityTier.TIER_4_STANDARD,
    "finance": PriorityTier.TIER_4_STANDARD,
    "business": PriorityTier.TIER_4_STANDARD,
    "education": PriorityTier.TIER_4_STANDARD,
    "learning": PriorityTier.TIER_4_STANDARD,
    "cooking": PriorityTier.TIER_4_STANDARD,
    "recipes": PriorityTier.TIER_4_STANDARD,
    "shopping": PriorityTier.TIER_4_STANDARD,
    "ecommerce": PriorityTier.TIER_4_STANDARD,
    "information": PriorityTier.TIER_4_STANDARD,
    "knowledge": PriorityTier.TIER_4_STANDARD,

    # Tier 5: Low
    "games": PriorityTier.TIER_5_LOW,
    "entertainment": PriorityTier.TIER_5_LOW,
    "fun": PriorityTier.TIER_5_LOW,
    "creative": PriorityTier.TIER_5_LOW,
    "art": PriorityTier.TIER_5_LOW,
    "social": PriorityTier.TIER_5_LOW,
    "trivia": PriorityTier.TIER_5_LOW,
    "jokes": PriorityTier.TIER_5_LOW,

    # Tier 6: Lazy
    "agriculture": PriorityTier.TIER_6_LAZY,
    "farming": PriorityTier.TIER_6_LAZY,
    "legal": PriorityTier.TIER_6_LAZY,
    "compliance": PriorityTier.TIER_6_LAZY,
    "automotive": PriorityTier.TIER_6_LAZY,
    "obd": PriorityTier.TIER_6_LAZY,
    "research": PriorityTier.TIER_6_LAZY,
    "science": PriorityTier.TIER_6_LAZY,
    "deep_learning": PriorityTier.TIER_6_LAZY,
}


def get_tier_for_skill(skill_name: str, category: Optional[str] = None) -> PriorityTier:
    """Determine the priority tier for a given skill name and category."""
    name_lower = skill_name.lower().replace("-", "_").replace(".", "_")
    cat_lower = (category or "").lower().replace("-", "_").replace(".", "_")

    # Check direct name matches
    for key, tier in DEFAULT_TIER_MAPPING.items():
        if key in name_lower:
            return tier

    # Check category matches
    if cat_lower and cat_lower in DEFAULT_TIER_MAPPING:
        return DEFAULT_TIER_MAPPING[cat_lower]

    return PriorityTier.TIER_4_STANDARD


def get_tier_priority(tier: PriorityTier) -> int:
    """Convert PriorityTier to numeric sort key (lower value = higher priority)."""
    return tier.value * 10
