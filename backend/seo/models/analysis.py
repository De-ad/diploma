from pydantic import BaseModel
from typing import Dict, List, Union
from datetime import datetime


class ErrorResult(BaseModel):
    error: str


class Check(BaseModel):
    found: bool = False
    message: str | None = None
    file_extension: str | None = None
    status_code: int | None = None
    error: str | None = None


class Metadata(BaseModel):
    title: str | None
    description: str | None


class Socials(BaseModel):
    title_value: str | None = None
    type_value: str | None = None
    description_value: str | None = None
    image_value: str | None = None
    url_value: str | None = None
    twitter_value: str | None = None


class SearchPreview(BaseModel):
    url: str
    title: str | None = None
    description: str | None = None
    has_favicon: bool
    date: datetime | None = None


class SeoFiles(BaseModel):
    robots: Check
    sitemap: Check
    favicon: Check


class SeoResult(BaseModel):
    seo_files: SeoFiles
    metadata: Union[Metadata, ErrorResult]
    socials: Union[Socials, ErrorResult]
    search_preview: Union[SearchPreview, ErrorResult]
    canonical_url: str | None = None
    structured_data: List[dict] = []
    charset: str | None = None
    doctype: str | None = None


class WordCloudResult(BaseModel):
    data: List[Dict[str, Union[str, int]]]


class PerformanceMetrics(BaseModel):
    performance_score: int
    first_contentful_paint: str
    largest_contentful_paint: str
    cumulative_layout_shift: str
    total_blocking_time: str
    speed_index: str


class ImageInfo(BaseModel):
    src: str
    size_kb: float


class AssetIssues(BaseModel):
    uncached_js: List[str]
    unminified_js: List[str]
    uncached_css: List[str]
    unminified_css: List[str]


class HtmlCompression(BaseModel):
    uncompressed_size_kb: float
    compressed_size_kb: float
    compression_type: str
    compression_rate_percent: float


class DataMetrics(BaseModel):
    dom_size: int
    html_compression: HtmlCompression
    total_images: int
    oversized_images: List[ImageInfo]
    uncached_images: List[str]
    asset_issues: AssetIssues


class Performance(BaseModel):
    mobile: PerformanceMetrics
    desktop: PerformanceMetrics
    data_metrics: DataMetrics


class BrokenLink(BaseModel):
    link: str
    error: str


class PageIssues(BaseModel):
    h1_missing: bool = False
    inline_code: bool = False
    image_seo: List[str] = []
    broken_links: List[BrokenLink] = []
    noindex: bool = False
    flash_content: bool = False
    frameset_used: bool = False
    unsafe_links: List[str] = []


class PageReport(BaseModel):
    url: str
    issues: PageIssues


class SslCertificate(BaseModel):
    subject: str
    issuer: str
    not_valid_before: str
    not_valid_after: str
    signature_algorithm: str
    version: str


class SslChecks(BaseModel):
    not_used_before_activation_date: bool
    not_expired: bool
    hostname_matches: bool
    trusted_by_major_browsers: bool
    uses_secure_hash: bool


class SslCertificatesAndChecks(BaseModel):
    server_certificate: SslCertificate
    intermediate_certificates: List[SslCertificate]
    root_certificate: SslCertificate
    checks: SslChecks


class SecurityAndServer(BaseModel):
    ssl_certificates: SslCertificatesAndChecks
    spf_record: Check
    all_unsafe_links: List[str]
    http2_support: bool


class Score(BaseModel):
    seo: int
    performance: int
    security: int


class Analysis(BaseModel):
    seo: SeoResult
    keywords_distribution: Union[dict, ErrorResult]
    wordcloud: Union[WordCloudResult, ErrorResult]
    performance: Union[Performance, ErrorResult]
    page_report: List[PageReport]
    security: SecurityAndServer
    score: Score
