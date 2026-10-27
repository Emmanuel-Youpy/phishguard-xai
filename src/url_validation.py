"""Shared URL input checks for the PhishGuard XAI Streamlit prototype.

Only http/https hostnames with alphabetic top-level domains are supported by
this existing prototype. This function does not check whether a URL is safe.
"""

import re
from urllib.parse import urlparse


_WARNING = "Please enter a URL."
_ERROR = (
    "Invalid URL. Please enter a valid web address, "
    "for example: https://www.example.com"
)


def is_valid_url(url: str) -> bool:
    try:
        url = str(url).strip()
        if not url or any(char.isspace() for char in url):
            return False
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        domain_pattern = (
            r"^(?!-)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*"
            r"\.[A-Za-z]{2,63}$"
        )
        if not re.fullmatch(domain_pattern, hostname):
            return False
        _ = parsed.port  # Evaluates and rejects malformed / out-of-range ports.
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def validate_url_input(url: str) -> tuple[str, str]:
    """Return (status, message) for the exact three input branches used by the UI.

    Status: 'warning' for an empty field, 'error' for invalid / unsupported,
    and 'valid' for an acceptable URL. Prediction is not executed here.
    """
    if not str(url or "").strip():
        return "warning", _WARNING
    if not is_valid_url(url):
        return "error", _ERROR
    return "valid", ""
