from pydantic import BaseModel
from typing import Dict, List, Union
from datetime import datetime

class ErrorResult(BaseModel):
    error: str
    
class CheckResult(BaseModel):
    found: bool
    message: str
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
        
class SeoResult(BaseModel):
    robots: Union[CheckResult, ErrorResult]
    sitemap: Union[CheckResult, ErrorResult]
    favicon: Union[CheckResult, ErrorResult]
    ssl_certificate: Union[CheckResult, ErrorResult]
    metadata: Union[Metadata, ErrorResult]
    socials: Union[Socials, ErrorResult]
    search_preview: Union[SearchPreview, ErrorResult]
    
class WordCloudResult(BaseModel):
    data: List[Dict[str, Union[str, int]]]

class Performance(BaseModel):
    performance_score: int
    first_contentful_paint: str
    largest_contentful_paint: str
    cumulative_layout_shift: str
    total_blocking_time: str
    
class Analysis(BaseModel):
    seo: SeoResult
    wordcloud: Union[WordCloudResult, ErrorResult]
    performance: Union [Performance, ErrorResult]
    page_report: list