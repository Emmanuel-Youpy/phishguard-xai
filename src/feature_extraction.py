from urllib.parse import urlparse
import re


# =========================================================
# V2 FEATURE COLUMNS
# Must match the model training features exactly
# =========================================================

FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "path_length",
    "query_length",
    "tld_length",
    "subdomain_count",
    "is_domain_ip",
    "digit_count",
    "letter_count",
    "dot_count",
    "hyphen_count",
    "underscore_count",
    "slash_count",
    "question_mark_count",
    "equals_count",
    "ampersand_count",
    "at_symbol_count",
    "percent_count",
    "special_char_count",
    "is_https"
]


def extract_url_features_v2(url):
    """
    Extract the 20 reproducible lexical and structural
    URL features used to train the V2 phishing model.
    """

    url = str(url).strip()

    # Add temporary scheme if one is missing.
    # This allows urlparse() to correctly identify the domain.
    parse_url = url

    if not re.match(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
        parse_url
    ):
        parse_url = "http://" + parse_url

    parsed = urlparse(parse_url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    clean_domain = hostname.lower()

    # Remove www. for consistent domain calculations
    if clean_domain.startswith("www."):
        clean_domain = clean_domain[4:]

    # Extract TLD
    tld = (
        clean_domain.rsplit(".", 1)[-1]
        if "." in clean_domain
        else ""
    )

    # Check whether hostname is an IPv4 address
    is_domain_ip = int(
        bool(
            re.fullmatch(
                r"\d{1,3}(?:\.\d{1,3}){3}",
                clean_domain
            )
        )
    )

    # Calculate number of subdomains
    domain_parts = [
        part
        for part in clean_domain.split(".")
        if part
    ]

    subdomain_count = max(
        len(domain_parts) - 2,
        0
    )

    features = {
        "url_length": len(url),
        "domain_length": len(clean_domain),
        "path_length": len(path),
        "query_length": len(query),
        "tld_length": len(tld),
        "subdomain_count": subdomain_count,
        "is_domain_ip": is_domain_ip,
        "digit_count": sum(c.isdigit() for c in url),
        "letter_count": sum(c.isalpha() for c in url),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "underscore_count": url.count("_"),
        "slash_count": url.count("/"),
        "question_mark_count": url.count("?"),
        "equals_count": url.count("="),
        "ampersand_count": url.count("&"),
        "at_symbol_count": url.count("@"),
        "percent_count": url.count("%"),
        "special_char_count": sum(
            not c.isalnum()
            for c in url
        ),
        "is_https": int(
            parsed.scheme.lower() == "https"
        )
    }

    return features


# Keep this function name for compatibility with app.py
def extract_url_features(url):
    return extract_url_features_v2(url)