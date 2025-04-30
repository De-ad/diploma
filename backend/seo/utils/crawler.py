
import asyncio
from typing import Union
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx
from models.analysis import ErrorResult, Metadata, SearchPreview, Socials
import json

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

async def check_link_status(client, url):
    try:
        resp = await client.head(url, timeout=10)
        if resp.status_code >= 400:
            return f"{resp.status_code} {resp.reason_phrase}"
        return None
    except Exception as e:
        return str(e)
   
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
        status = await check_link_status(client, next_url)
        if status:
            page_report["issues"].append(f"Broken link: {next_url} - {status}")
    await asyncio.gather(*tasks)
    
async def check_metadata(url: str,  client: httpx.AsyncClient) -> Union[Metadata, ErrorResult]:
    try:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = description_tag['content'] if description_tag else None
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
    
async def check_for_social_media_meta_tags(url: str,  client: httpx.AsyncClient):
    try:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_tag = soup.find("meta", attrs={"property": "og:title"})
            type_tag = soup.find("meta", attrs={"property": "og:type"})
            description_tag = soup.find("meta", attrs={"property": "og:description"})
            image_tag = soup.find("meta", attrs={"property": "og:image"})
            url_tag = soup.find("meta", attrs={"property": "og:url"})
            twitter_tag = soup.find("meta", attrs={"name": "twitter:card"})

            title = title_tag['content'] if title_tag and title_tag.has_attr('content') else None
            type = type_tag['content'] if type_tag and type_tag.has_attr('content') else None
            description = description_tag['content'] if description_tag and description_tag.has_attr('content') else None
            image = image_tag['content'] if image_tag and image_tag.has_attr('content') else None
            url = url_tag['content'] if url_tag and url_tag.has_attr('content') else None
            twitter = twitter_tag['content'] if twitter_tag and twitter_tag.has_attr('content') else None

            return Socials(
                title_value=title,
                title_found=bool(title),
                type_value=type,
                type_found=bool(type),
                description_value=description,
                description_found=bool(description),
                image_value=image,
                image_found=bool(image),
                url_value=url,
                url_found=bool(url),
                twitter_value=twitter,
                twitter_found=bool(twitter)
            )
                                
        else:
            return ErrorResult(error="Status code is not 200")
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))


async def get_serch_preview(url: str, client: httpx.AsyncClient, title: str, description_found: bool, description: str | None, has_favicon: bool,):
    try:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            if(not description_found):
                h1_tag = soup.find("h1")
                description = h1_tag.get_text(strip=True) if h1_tag else None
           
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    items = data if isinstance(data, list) else [data]

                    for item in items:
                        if isinstance(item, dict):
                            if '@graph' in item:
                                items.extend(item['@graph'])
                            date_published = item.get("datePublished")
                            date_created = item.get("dateCreated")
                            date = date_published or date_created
                            if date:
                                return SearchPreview(
                                    url=url,
                                    title=title,
                                    description=description,
                                    has_favicon=has_favicon,
                                    date=date
                                )
                except Exception:
                    continue 

        return SearchPreview(
            url=url,
            title=title,
            description=description,
            has_favicon=has_favicon,
            date=None
        )
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))
    