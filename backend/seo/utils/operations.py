from urllib.parse import urlparse
import httpx
import socket
import ssl
from typing import Union
from . import performance
from . import wordcloud
from . import crawler
from models.analysis import Analysis, CheckResult, ErrorResult, SeoFiles, SeoResult
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def analyze(url: str) -> Analysis:
    domain = urlparse(url).netloc
    async with httpx.AsyncClient(
        http2=True, follow_redirects=True, timeout=30
    ) as client:
        results = []
        await crawler.crawl(url, domain, client, results)

        robots_result = await check_file_exists(url, "robots.txt", client)
        sitemap_result = await check_file_exists(url, "sitemap.xml", client)
        favicon_result = await check_if_favicon_is_present(url, client)
        wordcloud_result = await wordcloud.create_word_cloud(url, client)
        keywords_destribution = await wordcloud.get_distribution_of_keywords(
            url, client
        )
        performance_result = await performance.check_performance_metrics(url, client)
        metadata_result = await crawler.check_metadata(url, client)
        ssl_result = await check_ssl_certificate(url)
        socials_result = await crawler.check_for_social_media_meta_tags(url, client)
        search_preview_result = await crawler.get_serch_preview(
            url,
            client,
            metadata_result.title_value,
            metadata_result.description_found,
            metadata_result.description_value,
            favicon_result.found,
        )

        return Analysis(
            seo=SeoResult(
                seo_files=SeoFiles(
                    robots=robots_result, sitemap=sitemap_result, favicon=favicon_result
                ),
                metadata=metadata_result,
                ssl_certificate=ssl_result,
                socials=socials_result,
                search_preview=search_preview_result,
            ),
            wordcloud=wordcloud_result,
            keywords_destribution=keywords_destribution,
            performance=performance_result,
            page_report=results,
        )


async def check_file_exists(
    url: str, filename: str, client: httpx.AsyncClient
) -> Union[CheckResult, ErrorResult]:
    file_url = f"{url.rstrip('/')}/{filename}"
    try:
        response = await client.get(file_url)
        found = response.status_code == 200
        return CheckResult(
            found=found,
            status_code=response.status_code,
            file_extension=None,
            message=f"{filename} {'found' if found else 'not found'}",
        )
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))


async def check_if_favicon_is_present(
    url: str, client: httpx.AsyncClient
) -> Union[CheckResult, ErrorResult]:
    favicon_extensions = ["ico", "png", "svg"]
    url = url.rstrip("/")
    for ext in favicon_extensions:
        favicon_url = f"{url}/favicon.{ext}"
        try:
            response = await client.get(favicon_url)
            if response.status_code == 200:
                return CheckResult(
                    found=True,
                    status_code=response.status_code,
                    file_extension=ext,
                    message=f"favicon.{ext} found",
                )
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

    return CheckResult(
        found=False, status_code=response.status_code, message="No favicon found"
    )


# should have clean url like example.com
# TODO: check not home page
async def check_ssl_certificate(url: str):
    clean_url = url.replace("http://", "").replace("https://", "").rstrip("/")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=clean_url) as s:
            s.connect((clean_url, 443))

        return CheckResult(
            found=True,
            status_code=200,
            message="Has valid ssl certificate",
            file_extension=None,
        )

    except Exception as e:
        return ErrorResult(error="Has invalid ssl certificate, error: " + str(e))
