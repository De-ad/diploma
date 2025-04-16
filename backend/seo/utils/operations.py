from bs4 import BeautifulSoup
import httpx
import socket
import ssl
import re
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import io
from typing import Union
import base64
from models.analysis import Analysis, Performance, CheckResult, ErrorResult, SeoResult, Metadata, WordCloudResult
import logging



async def analyze(url: str) -> Analysis:
    robots_result = await check_if_robots_file_is_present(url)
    favicon_result = await check_if_favicon_is_present(url)
    wordcloud_result = await create_word_cloud(url)
    performace_result = await check_performance_metrics(url)
    metadata_result = await check_metadata(url)
    ssl_result = await check_ssl_certificate(url)

    return Analysis(
        seo=SeoResult(
            robots=robots_result,
            favicon=favicon_result,
            metadata=metadata_result,
            ssl_certificate=ssl_result
        ),
        wordcloud=wordcloud_result,
        performance=performace_result,
        
    )

async def check_if_robots_file_is_present(url: str) -> Union[CheckResult, ErrorResult]:
    robots_url = f"{url.rstrip('/')}/robots.txt"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(robots_url)
            return CheckResult(
                found=response.status_code == 200,
                status_code=response.status_code,
                message="robots.txt is found" if response.status_code == 200 else "robots.txt not found"
            )
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

async def check_if_favicon_is_present(url: str) -> Union[CheckResult, ErrorResult]:
    favicon_extensions = ['ico', 'png', 'svg']
    url = url.rstrip('/')
    
    async with httpx.AsyncClient() as client:
        for ext in favicon_extensions:
            favicon_url = f"{url}/favicon.{ext}"
            try:
                response = await client.get(favicon_url)
                if response.status_code == 200:
                    return CheckResult(
                        found=True,
                        status_code=response.status_code,
                        message=f"favicon.{ext} found"
                    )
            except httpx.RequestError as e:
                return ErrorResult(error=str(e))
            
        return CheckResult(
                        found=False,
                        status_code=response.status_code,
                        message="No favicon found"
                    )
        
async def check_if_sitemap_file_is_present(url: str) -> Union[CheckResult, ErrorResult]:
    sitemap_url = f"{url.rstrip('/')}/sitemap.xml"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(sitemap_url)
            return CheckResult(
                found=response.status_code == 200,
                status_code=response.status_code,
                message="sitemap.xml is found" if response.status_code == 200 else "sitemap.xml not found"
            )
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

# should have clean url like example.com 
# TODO: check not home page 
async def check_ssl_certificate(url: str):
    clean_url = url.replace("http://", "").replace("https://", "").rstrip('/')
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=clean_url) as s:
            s.connect((clean_url, 443))

        return CheckResult(
                found=True,
                status_code=200,
                message="Has valid ssl certificate"
            )

    except Exception as e:
         return ErrorResult(error="Has invalid ssl certificate, error: " + str(e))


async def check_performance_metrics(url: str) -> Union[Performance, ErrorResult]:
    api_key = os.getenv("API_KEY")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
                fcp = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
                lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
                cls = data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
                tbt = data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

                return Performance(
                    performance_score= performance_score,
                    first_contentful_paint=fcp,
                    largest_contentful_paint= lcp,
                    cumulative_layout_shift=cls,
                    total_blocking_time=tbt
                )
            else:
                return ErrorResult(error="Status code is not 200")
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))
            

async def create_word_cloud(url: str) -> Union[WordCloudResult, ErrorResult]:
     async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                for tag in soup(['script', 'style', 'noscript']):
                    tag.decompose()

                text = soup.get_text(separator=' ', strip=True)
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

                img_io = io.BytesIO()
                wordcloud.to_image().save(img_io, format='PNG')
                img_io.seek(0)

                img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
                return WordCloudResult(
                    image= f"data:image/png;base64,{img_base64}"
                    )
                
            else:
                return ErrorResult(error="Status code is not 200")
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))
            


async def check_metadata(url) -> Union[Metadata, ErrorResult]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                description_tag = soup.find("meta", property="og:description")
                description = str(description_tag) if description_tag else None
                title_tag = soup.title
                title = title_tag.string.strip() if title_tag and title_tag.string else None
                
                return Metadata(
                    title_value=title,
                    title_found=bool(title),
                    description_found=bool(description),
                    description_value=description
                )
                                    
            else:
                return ErrorResult(error="Status code is not 200")
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

   

# inline css, deprecated, headers structure, image seo, 
def check_http_code(url):
    return