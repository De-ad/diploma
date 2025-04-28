
import asyncio
from typing import Union
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx
from models.analysis import ErrorResult, Metadata

visited = set()
semaphore = asyncio.Semaphore(10)

async def fetch(client, url):
    try:
        async with semaphore:
            response = await client.get(url, timeout=10)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return None
            return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def estimate_image_is_large(img_tag):
    src = img_tag.get("src", "")
    return any(x in src.lower() for x in ["large", "hero", "banner"]) or \
           any(x in src.lower() for x in ["800", "1024", "1920", "2048"])  

async def crawl(url, domain, client, results):
    page_report = {
            "url": url,
            "issues": []
        }
    if url in visited:
        return
    visited.add(url)

    html = await fetch(client, url)
    if not html:
        return

    soup = BeautifulSoup(html, 'html.parser')
        
    for img in soup.find_all('img'):
        if 'alt' not in img.attrs:
            results.append({
                "url": url,
                "image_snippet": str(img)[:150]
            })
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 0:
        page_report["issues"].append("Missing <h1> tag")
    elif len(h1_tags) > 1:
        page_report["issues"].append("Multiple <h1> tags")

    if soup.find('style') or soup.find('script'):
        page_report["issues"].append("Inline <style> or <script> found")
    large_images = []
    for img in soup.find_all('img'):
        if estimate_image_is_large(img):
            large_images.append(img.get("src", "")[:100])
    if large_images:
        page_report["issues"].append(f"Potential large images: {large_images[:3]}")
        
    if not soup.find('meta', attrs={"name": "viewport"}):
        page_report["issues"].append("Missing viewport meta tag (mobile-unfriendly)")

    if page_report["issues"]:
        results.append(page_report)

    tasks = []
    for link in soup.find_all('a', href=True):
        next_url = urljoin(url, link['href'])
        if urlparse(next_url).netloc == domain and next_url not in visited:
            tasks.append(crawl(next_url, domain, client, results))

    await asyncio.gather(*tasks)
    
async def check_metadata(url: str,  client: httpx.AsyncClient) -> Union[Metadata, ErrorResult]:
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
