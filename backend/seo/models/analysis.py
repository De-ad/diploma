from pydantic import BaseModel
from typing import Dict, List, Union

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
    
class SeoResult(BaseModel):
    robots: Union[CheckResult, ErrorResult]
    sitemap: Union[CheckResult, ErrorResult]
    favicon: Union[CheckResult, ErrorResult]
    ssl_certificate: Union[CheckResult, ErrorResult]
    metadata: Union[Metadata, ErrorResult]
    
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