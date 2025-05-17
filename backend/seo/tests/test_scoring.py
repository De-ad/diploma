import pytest
from unittest.mock import Mock
from utils.scoring import get_performance_score, get_security_score, get_seo_score
from models.analysis import Performance, SecurityAndServer, Check, WordCloudResult

@pytest.fixture
def mock_seo_result():
    seo_result = Mock()
    
    seo_result.seo_files.robots.found = True
    seo_result.seo_files.sitemap.found = True
    seo_result.seo_files.favicon.found = True
    seo_result.metadata.title = "Test Title"
    seo_result.metadata.description = "Test Description"
    seo_result.socials.dict.return_value = {"title_value": "Test Social"}
    seo_result.canonical_url = "http://example.com"
    seo_result.structured_data = [{"type": "type1"}]
    seo_result.charset = "UTF-8"
    seo_result.doctype = "html"
    
    return seo_result


@pytest.fixture
def mock_page_report():
    page_report = [Mock()]
    page_report[0].issues.h1_missing = False
    page_report[0].issues.inline_code = True
    page_report[0].issues.image_seo = False
    page_report[0].issues.broken_links = False
    page_report[0].issues.noindex = False
    return page_report


@pytest.fixture
def mock_performance():
    performance = Mock(spec=Performance)
    performance.desktop.performance_score = 80
    performance.mobile.performance_score = 85
    performance.data_metrics.dom_size = 1200
    performance.data_metrics.oversized_images = ["img1", "img2"]
    performance.data_metrics.uncached_images = ["img3"]
    performance.data_metrics.asset_issues.uncached_js = ["js1"]
    performance.data_metrics.asset_issues.unminified_js = ["js2"]
    performance.data_metrics.asset_issues.uncached_css = ["css1"]
    performance.data_metrics.asset_issues.unminified_css = ["css2"]
    performance.data_metrics.html_compression.compression_type = "gzip"
    performance.data_metrics.html_compression.compression_rate_percent = 30
    return performance


@pytest.fixture
def mock_security():
    ssl_certificate = Mock()
    ssl_certificate.subject = "example.com"
    ssl_certificate.issuer = "CA"
    ssl_certificate.not_valid_before = "2025-01-01"
    ssl_certificate.not_valid_after = "2026-01-01"
    ssl_certificate.signature_algorithm = "RSA"
    ssl_certificate.version = "3"

    ssl_checks = Mock()
    ssl_checks.not_used_before_activation_date = True
    ssl_checks.not_expired = True
    ssl_checks.hostname_matches = True
    ssl_checks.trusted_by_major_browsers = True
    ssl_checks.uses_secure_hash = True

    spf_record = Mock(spec=Check)
    spf_record.found = True
    
    security = Mock(spec=SecurityAndServer)
    security.ssl_certificates.checks = ssl_checks
    security.ssl_certificates.server_certificate = ssl_certificate
    security.ssl_certificates.intermediate_certificates = [ssl_certificate]
    security.ssl_certificates.root_certificate = ssl_certificate
    security.spf_record = spf_record
    security.all_unsafe_links = []
    security.http2_support = True
    
    return security


def test_get_seo_score(mock_seo_result, mock_page_report):
    score = get_seo_score(mock_seo_result, mock_page_report)
    assert score == 100  


def test_get_performance_score(mock_performance):
    score = get_performance_score(mock_performance)
    assert 0 <= score <= 100 


def test_get_security_score(mock_security):
    score = get_security_score(mock_security)
    assert 0 <= score <= 100  


def test_get_seo_score_with_missing_robots(mock_seo_result, mock_page_report):
    mock_seo_result.seo_files.robots.found = False
    score = get_seo_score(mock_seo_result, mock_page_report)
    assert score < 100 


def test_get_performance_score_with_high_dom_size(mock_performance):
    mock_performance.data_metrics.dom_size = 1600  
    score = get_performance_score(mock_performance)
    assert score < 100 


def test_get_security_score_with_unsafe_links(mock_security):
    mock_security.all_unsafe_links = ["http://unsafe.com"]
    score = get_security_score(mock_security)
    assert score < 100  
