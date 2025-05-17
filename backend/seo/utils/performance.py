import os
from typing import List, Union
from urllib.parse import urljoin
import httpx
from models.analysis import (
    AssetIssues,
    DataMetrics,
    ErrorResult,
    HtmlCompression,
    ImageInfo,
    Performance,
    PerformanceMetrics,
)
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


async def fetch_performance_data(
    url: str, client: httpx.AsyncClient, strategy: str
) -> Union[PerformanceMetrics, ErrorResult]:
    api_key = os.getenv("GOOGLE_API_KEY")
    api_url = (
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&key={api_key}&strategy={strategy}&category=performance"
    )
    try:
        response = await client.get(api_url)
        data = response.json()

        if response.status_code == 200:
            try:
                return PerformanceMetrics(
                    performance_score=int(
                        data["lighthouseResult"]["categories"]["performance"]["score"]
                        * 100
                    ),
                    first_contentful_paint=data["lighthouseResult"]["audits"][
                        "first-contentful-paint"
                    ]["displayValue"],
                    largest_contentful_paint=data["lighthouseResult"]["audits"][
                        "largest-contentful-paint"
                    ]["displayValue"],
                    cumulative_layout_shift=data["lighthouseResult"]["audits"][
                        "cumulative-layout-shift"
                    ]["displayValue"],
                    total_blocking_time=data["lighthouseResult"]["audits"][
                        "total-blocking-time"
                    ]["displayValue"],
                    speed_index=data["lighthouseResult"]["audits"]["speed-index"][
                        "displayValue"
                    ],
                )
            except (KeyError, TypeError) as parse_error:
                return ErrorResult(
                    error=f"Failed to parse {strategy} performance data: {parse_error}"
                )
        else:
            return ErrorResult(
                error=f"{strategy.capitalize()} status code is not 200: {response.status_code}"
            )
    except httpx.RequestError as e:
        return ErrorResult(
            error=f"{strategy.capitalize()} request error: {type(e).__name__}: {e}"
        )


async def check_performance_metrics(
    url: str, client: httpx.AsyncClient
) -> Union[Performance, ErrorResult]:
    mobile_result = await fetch_performance_data(url, client, "mobile")
    desktop_result = await fetch_performance_data(url, client, "desktop")

    if isinstance(mobile_result, ErrorResult):
        return mobile_result
    if isinstance(desktop_result, ErrorResult):
        return desktop_result
    data_metrics = await get_data_metrics(url, client)
    return Performance(
        mobile=mobile_result, desktop=desktop_result, data_metrics=data_metrics
    )


async def check_image_metadata_and_caching(soup, base_url, client):
    img_tags = soup.find_all("img", src=True)
    total_images = len(img_tags)
    oversized_images = []
    uncached_images = []

    for img in img_tags:
        src = urljoin(base_url, img["src"])
        try:
            response = await client.get(src, timeout=10)
            img_data = response.content
            size_kb = len(img_data) / 1024

            if size_kb > 200:
                oversized_images.append((src, size_kb))

            headers = response.headers
            cache_control = headers.get("Cache-Control", "")
            if not any(
                token in cache_control.lower()
                for token in ["max-age", "public", "immutable"]
            ):
                uncached_images.append(src)

            try:
                with Image.open(BytesIO(img_data)) as im:
                    _ = im.size  
            except Exception:
                continue

        except Exception:
            continue

    return total_images, oversized_images, uncached_images


async def analyze_assets(urls: List[str], client: httpx.AsyncClient):
    uncached, unminified = [], []
    for url in urls:
        try:
            response = await client.get(url, timeout=10)
            headers = response.headers
            cache_control = headers.get("Cache-Control", "")
            if not any(
                token in cache_control.lower()
                for token in ["max-age", "public", "immutable"]
            ):
                uncached.append(url)

            content = response.text
            if max((len(line) for line in content.splitlines()), default=0) > 200:
                unminified.append(url)

        except Exception:
            continue

    return uncached, unminified


async def check_static_asset_caching_and_minification(soup, base_url, client):
    js_files = [
        urljoin(base_url, tag["src"]) for tag in soup.find_all("script", src=True)
    ]
    css_files = [
        urljoin(base_url, tag["href"])
        for tag in soup.find_all("link", rel="stylesheet", href=True)
    ]

    uncached_js, unmin_js = await analyze_assets(js_files, client)
    uncached_css, unmin_css = await analyze_assets(css_files, client)

    return {
        "uncached_js": uncached_js,
        "unminified_js": unmin_js,
        "uncached_css": uncached_css,
        "unminified_css": unmin_css,
    }


async def check_html_compression_and_size(url, client):
    headers = {"Accept-Encoding": "gzip, deflate, br"}
    response = await client.get(url, headers=headers, timeout=10)
    compressed_size = int(response.headers.get("Content-Length", len(response.content)))
    html = response.text
    uncompressed_size = len(html.encode("utf-8"))
    compression_type = response.headers.get("Content-Encoding", "none")
    compression_rate = (
        100 - ((compressed_size / uncompressed_size) * 100) if uncompressed_size else 0
    )
    return html, uncompressed_size, compressed_size, compression_type, compression_rate


def get_dom_size(soup: BeautifulSoup) -> int:
    return len(soup.find_all())


async def get_data_metrics(url: str, client: httpx.AsyncClient) -> DataMetrics:
    (
        html,
        uncompressed_size,
        compressed_size,
        compression_type,
        compression_rate,
    ) = await check_html_compression_and_size(url, client)
    soup = BeautifulSoup(html, "html.parser")

    dom_elements = get_dom_size(soup)
    (
        total_images,
        oversized_images_raw,
        uncached_images,
    ) = await check_image_metadata_and_caching(soup, url, client)
    oversized_images = [
        ImageInfo(src=src, size_kb=kb) for src, kb in oversized_images_raw
    ]

    asset_data = await check_static_asset_caching_and_minification(soup, url, client)
    asset_issues = AssetIssues(**asset_data)

    return DataMetrics(
        dom_size=dom_elements,
        html_compression=HtmlCompression(
            uncompressed_size_kb=uncompressed_size / 1024,
            compressed_size_kb=compressed_size / 1024,
            compression_type=compression_type,
            compression_rate_percent=round(compression_rate, 2),
        ),
        total_images=total_images,
        oversized_images=oversized_images,
        uncached_images=uncached_images,
        asset_issues=asset_issues,
    )
