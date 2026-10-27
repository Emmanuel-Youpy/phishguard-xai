"""Human-readable LIME bin conditions, preserving inequality direction.

LIME's conditions denote intervals (e.g. `0 < dot_count <= 2`). A prior
formatter removed the inequality signs and incorrectly labelled every
condition 'or fewer', even for `>` or bounded intervals.
"""

import re

FEATURE_LABELS = {
    "url_length": "URL length",
    "domain_length": "Domain length",
    "path_length": "Path length",
    "query_length": "Query length",
    "tld_length": "Top-level domain length",
    "subdomain_count": "Number of subdomains",
    "is_domain_ip": "Domain is an IP address",
    "digit_count": "Number of digits",
    "letter_count": "Number of letters",
    "dot_count": "Number of dots",
    "hyphen_count": "Number of hyphens",
    "underscore_count": "Number of underscores",
    "slash_count": "Number of slashes",
    "question_mark_count": "Number of question marks",
    "equals_count": "Number of equals signs",
    "ampersand_count": "Number of ampersands",
    "at_symbol_count": "Number of @ symbols",
    "percent_count": "Number of % symbols",
    "special_char_count": "Number of special characters",
    "is_https": "Uses HTTPS",
}


def _tidy_number(match: re.Match) -> str:
    raw = match.group(0)
    try:
        result = float(raw)
    except ValueError:
        return raw
    if result.is_integer():
        return str(int(result))
    return f"{result:g}"


def format_lime_condition(condition: str) -> str:
    """Keep `<`, `<=`, `>` and `>=` logically accurate in tables and plots.

    Returns a *description of LIME's threshold*, not a safety rule.
    """
    readable = str(condition)
    for source, friendly in FEATURE_LABELS.items():
        readable = re.sub(
            rf"(?<![\w]){re.escape(source)}(?![\w])",
            lambda match, replacement=friendly: replacement,
            readable,
        )
    # LIME produces decimal thresholds; shorten only trailing zeroes.
    readable = re.sub(r"(?<![\w])-?\d+\.\d+(?![\w])", _tidy_number, readable)
    for operator, symbol in [("<=", "≤"), (">=", "≥"), ("<", "<"), (">", ">")]:
        # process two-character operators before their one-character counterparts
        if len(operator) == 2:
            readable = re.sub(rf"\s*{re.escape(operator)}\s*", f" {symbol} ", readable)
    readable = re.sub(r"\s*(?<![<>=])<(?![=])\s*", " < ", readable)
    readable = re.sub(r"\s*(?<![<>=])>(?![=])\s*", " > ", readable)
    return " ".join(readable.split())
