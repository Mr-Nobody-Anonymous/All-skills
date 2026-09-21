"""
Data Format and Type Conversion Utilities.
"""

from typing import Any, Dict

def to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "y", "on")
    return bool(val)

def to_int(val: Any, default: int = 0) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def to_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def dict_to_xml(tag: str, d: Dict[str, Any]) -> str:
    elem = f"<{tag}>\n"
    for key, val in d.items():
        elem += f"  <{key}>{val}</{key}>\n"
    elem += f"</{tag}>"
    return elem

def xml_to_dict(xml_str: str) -> Dict[str, Any]:
    # Lightweight XML parser fallback
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}
