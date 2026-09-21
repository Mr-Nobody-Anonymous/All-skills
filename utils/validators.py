"""
Data and Input Validation Utilities.
"""

import re
import json
from typing import Any

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
URL_REGEX = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

def validate_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def validate_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    return bool(URL_REGEX.match(url.strip()))

def validate_json(data_str: str) -> bool:
    try:
        json.loads(data_str)
        return True
    except (ValueError, TypeError):
        return False
