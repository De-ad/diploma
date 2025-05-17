import asyncio
from typing import Union
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx
from models.analysis import (
    BrokenLink,
    Check,
    ErrorResult,
    Metadata,
    PageIssues,
    PageReport,
    SearchPreview,
    Socials,
)
import json
from dateutil.parser import parse as parse_date
import re
import dns.resolver

semaphore = asyncio.Semaphore(10)


async def fetch(client, url):
    try:
        async with semaphore:
            response = await client.get(url, timeout=10)
            if "text/html" not in response.headers.get("Content-Type", ""):
                return None
            return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def estimate_image_is_large(img_tag):
    src = img_tag.get("src", "")
    return any(x in src.lower() for x in ["large", "hero", "banner"]) or any(
        x in src.lower() for x in ["800", "1024", "1920", "2048"]
    )


async def check_link_status(client, url):
    try:
        resp = await client.head(url, timeout=10)
        if resp.status_code >= 400:
            return f"{resp.status_code} {resp.reason_phrase}"
        return None
    except Exception as e:
        return str(e)


async def crawl(url, domain, client, results, visited, all_unsafe_links):
    if url in visited:
        return
    visited.add(url)

    html = await fetch(client, url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")
    issues = PageIssues()

    # Image SEO (missing alt attribute)
    image_snippets = [
        str(img)[:150] for img in soup.find_all("img") if "alt" not in img.attrs
    ]
    if image_snippets:
        issues.image_seo = image_snippets

    # H1 tag check
    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.h1_missing = True

    # Check for inline <style> or <script>
    if soup.find("style") or soup.find("script"):
        issues.inline_code = True

    # Check for broken links
    broken_links = []
    tasks = []
    for link in soup.find_all("a", href=True):
        next_url = urljoin(url, link["href"])
        if urlparse(next_url).netloc == domain and next_url not in visited:
            tasks.append(
                crawl(next_url, domain, client, results, visited, all_unsafe_links)
            )

        status = await check_link_status(client, next_url)
        if status:
            broken_links.append(BrokenLink(link=next_url, error=status))
    if broken_links:
        issues.broken_links = broken_links

    # Check for noindex tag
    if check_noindex_tag(soup):
        issues.noindex = True

    # Check for flash content
    if check_flash_content(soup):
        issues.flash_content = True

    # Check for frameset usage
    if check_frameset_usage(soup):
        issues.frameset_used = True

    # Check for unsafe cross-origin links
    unsafe_links = check_unsafe_cross_origin_links(soup, url)
    if unsafe_links:
        issues.unsafe_links = unsafe_links
        all_unsafe_links.update(unsafe_links)

    # Create the dictionary dynamically to only include non-empty fields
    issues_dict = {
        key: value
        for key, value in issues.dict().items()
        if value not in [False, [], None]
    }

    if issues_dict:
        results.append(PageReport(url=url, issues=issues_dict))

    await asyncio.gather(*tasks)


async def check_metadata(soup) -> Union[Metadata, ErrorResult]:
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"] if description_tag else None
    title_tag = soup.title
    title = title_tag.string.strip() if title_tag and title_tag.string else None

    return Metadata(
        title=title,
        description=description,
    )


async def check_for_social_media_meta_tags(soup):
    title_tag = soup.find("meta", attrs={"property": "og:title"})
    type_tag = soup.find("meta", attrs={"property": "og:type"})
    description_tag = soup.find("meta", attrs={"property": "og:description"})
    image_tag = soup.find("meta", attrs={"property": "og:image"})
    url_tag = soup.find("meta", attrs={"property": "og:url"})
    twitter_tag = soup.find("meta", attrs={"name": "twitter:card"})

    title = (
        title_tag["content"] if title_tag and title_tag.has_attr("content") else None
    )
    type = type_tag["content"] if type_tag and type_tag.has_attr("content") else None
    description = (
        description_tag["content"]
        if description_tag and description_tag.has_attr("content")
        else None
    )
    image = (
        image_tag["content"] if image_tag and image_tag.has_attr("content") else None
    )
    url = url_tag["content"] if url_tag and url_tag.has_attr("content") else None
    twitter = (
        twitter_tag["content"]
        if twitter_tag and twitter_tag.has_attr("content")
        else None
    )

    return Socials(
        title_value=title,
        type_value=type,
        description_value=description,
        image_value=image,
        url_value=url,
        twitter_value=twitter,
    )


async def get_serch_preview(
    url: str,
    soup,
    title: str,
    description: str | None,
    has_favicon: bool,
):
    scripts = soup.find_all("script", type="application/ld+json")
    if not description:
        h1_tag = soup.find("h1")
        description = h1_tag.get_text(strip=True) if h1_tag else None

    for script in scripts:
        try:
            data = json.loads(script.string)
            items = data if isinstance(data, list) else [data]

            for item in items:
                if isinstance(item, dict):
                    if "@graph" in item:
                        items.extend(item["@graph"])
                    date_published = item.get("datePublished")
                    date_created = item.get("dateCreated")
                    date = date_published or date_created
                    try:
                        parsed_date = parse_date(date)
                    except Exception:
                        parsed_date = None
                    if date:
                        return SearchPreview(
                            url=url,
                            title=title,
                            description=description,
                            has_favicon=has_favicon,
                            date=parsed_date,
                        )
        except Exception:
            continue

    return SearchPreview(
        url=url,
        title=title,
        description=description,
        has_favicon=has_favicon,
        date=None,
    )


async def check_http2_support(url: str, client: httpx.AsyncClient):
    try:
        response = await client.get(url)
        return response.http_version == "HTTP/2"
    except Exception as e:
        print("HTTP/2 check failed:", e)
        return False


def check_unsafe_cross_origin_links(soup, base_url):
    unsafe_links = []
    base_domain = urlparse(base_url).netloc
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            link_domain = urlparse(href).netloc
            if link_domain != base_domain and a.get("rel") != [
                "noopener",
                "noreferrer",
            ]:
                unsafe_links.append(href)
    return unsafe_links


def check_canonical_tag(soup):
    canonical = soup.find("link", rel="canonical")
    return canonical["href"] if canonical else None


def check_structured_data(soup):
    structured = soup.find_all("script", type="application/ld+json")
    return [s.get_text() for s in structured]


def check_flash_content(soup):
    return bool(
        soup.find_all("object", type="application/x-shockwave-flash")
        or soup.find_all("embed", type="application/x-shockwave-flash")
    )


def check_frameset_usage(soup):
    return bool(soup.find_all("frameset"))


def check_noindex_tag(soup):
    noindex = soup.find("meta", attrs={"name": "robots"})
    if noindex and "noindex" in noindex.get("content", "").lower():
        return True
    return False


async def check_spf_record(domain: str) -> bool:
    return await asyncio.to_thread(_check_spf_record_sync, domain)


def _check_spf_record_sync(domain) -> Check:
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        for rdata in answers:
            for txt_string in rdata.strings:
                if isinstance(txt_string, bytes):
                    txt_string = txt_string.decode()
                if "v=spf1" in txt_string:
                    return Check(found=True, message=txt_string)
    except Exception as e:
        print("SPF check error:", e)
        return Check(found=False, error=str(e))

    return Check(found=False, message="No SPF record found")


def check_doctype(html_text: str) -> str | None:
    match = re.match(r"(?i)<!doctype\s+html.*?>", html_text.strip())
    return match.group(0) if match else None


def check_charset(soup):
    meta = soup.find("meta", charset=True)
    if meta:
        return meta["charset"]
    meta = soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if meta and "charset=" in meta.get("content", "").lower():
        return meta["content"]
    return None


def check_deprecated_html(soup):
    deprecated_tags = ["font", "center", "marquee", "bgsound", "blink"]
    found = []
    for tag in deprecated_tags:
        if soup.find(tag):
            found.append(tag)
    return found
