from models.analysis import Performance, SecurityAndServer


def get_seo_score(seo, page_report):
    seo_weights = {
        "robots": 10,
        "sitemap": 10,
        "favicon": 2,
        "title": 10,
        "description": 6,
        "socials": 5,
        "canonical_url": 6,
        "structured_data": 5,
        "charset": 3,
        "doctype": 3,
        "h1_missing": 6,
        "inline_code": 3,
        "image_seo": 4,
        "broken_links": 8,
        "noindex": 10,
    }

    deductions = 0

    if not seo.seo_files.robots.found:
        deductions += seo_weights["robots"]
    if not seo.seo_files.sitemap.found:
        deductions += seo_weights["sitemap"]
    if not seo.seo_files.favicon.found:
        deductions += seo_weights["favicon"]
    if not seo.metadata.title:
        deductions += seo_weights["title"]
    if not seo.metadata.description:
        deductions += seo_weights["description"]

    if all(value is None for value in seo.socials.dict().values()):
        deductions += seo_weights["socials"]

    if seo.canonical_url is None:
        deductions += seo_weights["canonical_url"]

    if len(seo.structured_data) == 0:
        deductions += seo_weights["structured_data"]

    if not seo.charset:
        deductions += seo_weights["charset"]
    if not seo.doctype:
        deductions += seo_weights["doctype"]

    page_issues_flags = {
        "h1_missing": False,
        "inline_code": False,
        "image_seo": False,
        "broken_links": False,
        "noindex": False,
    }

    for page in page_report:
        issues = page.issues.dict() if hasattr(page.issues, "dict") else page.issues
        for key in page_issues_flags:
            if issues.get(key):
                page_issues_flags[key] = True

    for issue, happened in page_issues_flags.items():
        if happened:
            deductions += seo_weights[issue]

    return max(0, 100 - deductions)

def get_performance_score(performance: Performance) -> int:
    deductions = 0

    lighthouse_weight = 30  
    desktop_penalty = 100 - performance.desktop.performance_score
    mobile_penalty = 100 - performance.mobile.performance_score
    average_penalty = (desktop_penalty + mobile_penalty) / 2
    deductions += (average_penalty / 100) * lighthouse_weight

    if performance.data_metrics.dom_size > 1500:
        deductions += 5
    elif performance.data_metrics.dom_size > 1000:
        deductions += 3
    elif performance.data_metrics.dom_size > 500:
        deductions += 1

    if performance.data_metrics.oversized_images:
        deductions += min(len(performance.data_metrics.oversized_images), 5)

    if performance.data_metrics.uncached_images:
        deductions += min(len(performance.data_metrics.uncached_images), 5)

    asset_issues = performance.data_metrics.asset_issues
    js_css_penalty = sum([
        len(asset_issues.uncached_js),
        len(asset_issues.unminified_js),
        len(asset_issues.uncached_css),
        len(asset_issues.unminified_css),
    ])
    deductions += min(js_css_penalty, 10)

    compression = performance.data_metrics.html_compression
    if compression.compression_type == "none":
        deductions += 5
    elif compression.compression_rate_percent < 20:
        deductions += 3
    elif compression.compression_rate_percent < 40:
        deductions += 1

    return max(0, int(100 - deductions))


def get_security_score(security: SecurityAndServer) -> int:
    deductions = 0
    
    ssl_checks = security.ssl_certificates.checks
    ssl_deduction_map = {
        "not_used_before_activation_date": 5,
        "not_expired": 10,
        "hostname_matches": 10,
        "trusted_by_major_browsers": 15,
        "uses_secure_hash": 10,
    }

    for check, penalty in ssl_deduction_map.items():
        if not getattr(ssl_checks, check):
            deductions += penalty

    if not security.spf_record.found:
        deductions += 10
        
    if security.all_unsafe_links:
        # Deduct 2 points per unsafe link, up to 10
        deductions += min(len(security.all_unsafe_links) * 2, 10)

    if not security.http2_support:
        deductions += 10

    return max(0, int(100 - deductions))
