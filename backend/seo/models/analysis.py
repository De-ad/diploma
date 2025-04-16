from pydantic import BaseModel
from typing import Union

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
    favicon: Union[CheckResult, ErrorResult]
    ssl_certificate: Union[CheckResult, ErrorResult]
    metadata: Union[Metadata, ErrorResult]
    

class WordCloudResult(BaseModel):
    image: str

class Performance(BaseModel):
    performance_score: int
    first_contentful_paint: int
    largest_contentful_paint: int
    cumulative_layout_shift: int
    total_blocking_time: int
    
class Analysis(BaseModel):
    seo: SeoResult
    wordcloud: Union[WordCloudResult, ErrorResult]
    performance: Union [Performance, ErrorResult]