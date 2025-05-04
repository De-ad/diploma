from pydantic import BaseModel
from typing import Dict, List, Union
from datetime import datetime


class ErrorResult(BaseModel):
    error: str


class CheckResult(BaseModel):
    found: bool
    message: str
    file_extension: str | None
    status_code: int


class Metadata(BaseModel):
    title_value: str | None
    title_found: bool
    description_value: str | None
    description_found: bool


class Socials(BaseModel):
    title_value: str | None = None
    title_found: bool = False
    type_value: str | None = None
    type_found: bool = False
    description_value: str | None = None
    description_found: bool = False
    image_value: str | None = None
    image_found: bool = False
    url_value: str | None = None
    url_found: bool = False
    twitter_value: str | None = None
    twitter_found: bool = False


class SearchPreview(BaseModel):
    url: str
    title: str | None = None
    description: str | None = None
    has_favicon: bool
    date: datetime | None = None


class SeoFiles(BaseModel):
    robots: Union[CheckResult, ErrorResult]
    sitemap: Union[CheckResult, ErrorResult]
    favicon: Union[CheckResult, ErrorResult]


class SeoResult(BaseModel):
    seo_files: SeoFiles
    ssl_certificate: Union[CheckResult, ErrorResult]
    metadata: Union[Metadata, ErrorResult]
    socials: Union[Socials, ErrorResult]
    search_preview: Union[SearchPreview, ErrorResult]


class WordCloudResult(BaseModel):
    data: List[Dict[str, Union[str, int]]]


class PerformanceMetrics(BaseModel):
    performance_score: int
    first_contentful_paint: str
    largest_contentful_paint: str
    cumulative_layout_shift: str
    total_blocking_time: str
    speed_index: str


class Performance(BaseModel):
    mobile: PerformanceMetrics
    desktop: PerformanceMetrics


class BrokenLink(BaseModel):
    link: str
    error: str


class PageIssues(BaseModel):
    h1_missing: Union[bool, None] = None
    inline_code: Union[bool, None] = None
    image_seo: Union[List[str], None] = None
    broken_links: Union[List[BrokenLink], None] = None


class PageReport(BaseModel):
    url: str
    issues: PageIssues


class Analysis(BaseModel):
    seo: SeoResult
    keywords_destribution: Union[dict, ErrorResult]
    wordcloud: Union[WordCloudResult, ErrorResult]
    performance: Union[Performance, ErrorResult]
    page_report: List[PageReport]
