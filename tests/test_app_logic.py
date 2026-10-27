"""Run: python -m pytest tests/test_app_logic.py -v

These tests exercise the exact functions imported by app.py. They do NOT claim
that SHAP/LIME UI rendering or the deployed pickle has been executed.
"""

import ast
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from feature_extraction import FEATURE_NAMES, extract_url_features
from lime_formatting import FEATURE_LABELS, format_lime_condition
from url_validation import is_valid_url, validate_url_input


def test_tc03_empty_url_warning():
    assert validate_url_input("") == ("warning", "Please enter a URL.")
    assert validate_url_input("   ") == ("warning", "Please enter a URL.")


def test_tc04_invalid_domain_rejection():
    status, message = validate_url_input("hello12354")
    assert status == "error" and "Invalid URL" in message
    assert not is_valid_url("https://example")


def test_tc05_unsupported_scheme_rejection():
    for url in ("ftp://example.com", "file://example.com", "javascript:alert(1)"):
        status, message = validate_url_input(url)
        assert status == "error" and "Invalid URL" in message


def test_tc05_bad_port_and_whitespace_rejection():
    for url in ("https://example.com:70000", "https://exa mple.com"):
        assert not is_valid_url(url)


def test_valid_http_https_submission():
    for url in ("https://www.google.com", "http://example.com", "https://example.co.uk/path?q=1"):
        assert validate_url_input(url) == ("valid", "")


def test_feature_extraction_retains_20_features_and_https():
    url = "https://www.example.com/a?q=1"
    features = extract_url_features(url)
    assert list(features) == FEATURE_NAMES
    assert len(features) == 20
    assert features["is_https"] == 1
    assert features["slash_count"] == url.count("/")


def test_lime_lower_or_equal_direction():
    assert format_lime_condition("slash_count <= 2.00") == "Number of slashes ≤ 2"


def test_lime_strict_lower_direction():
    assert format_lime_condition("dot_count < 3.00") == "Number of dots < 3"


def test_lime_strict_greater_direction():
    assert format_lime_condition("dot_count > 2.00") == "Number of dots > 2"


def test_lime_greater_or_equal_direction():
    assert format_lime_condition("digit_count >= 1.00") == "Number of digits ≥ 1"


def test_lime_double_bounded_interval():
    assert format_lime_condition("0.00 < subdomain_count <= 1.00") == "0 < Number of subdomains ≤ 1"
    assert format_lime_condition("12.00 < domain_length <= 16.00") == "12 < Domain length ≤ 16"


def test_lime_decimal_and_binary():
    assert format_lime_condition("is_https <= 0.50") == "Uses HTTPS ≤ 0.5"
    assert format_lime_condition("0.00 < is_domain_ip <= 1.00") == "0 < Domain is an IP address ≤ 1"


def test_lime_original_chart_case_is_not_mislabeled():
    original = "0.00 < subdomain_count <= 1.00"
    result = format_lime_condition(original)
    assert result == "0 < Number of subdomains ≤ 1"
    assert "or fewer" not in result


def test_ui_source_reuses_tested_helpers_in_both_lime_outputs():
    app_source = (PROJECT_ROOT / "app/app.py").read_text(encoding="utf-8")
    ast.parse(app_source)
    assert "validate_url_input(url)" in app_source
    assert '].apply(format_lime_condition)' in app_source
    assert "format_lime_condition(item[0]) for item in lime_chart_data" in app_source
    assert "def make_lime_condition_readable" not in app_source
    assert app_source.index("st.set_page_config(") < app_source.index("load_css()")
