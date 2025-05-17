from urllib.parse import urlparse
from bs4 import BeautifulSoup
import httpx
from typing import Union

from utils.scoring import get_performance_score, get_security_score, get_seo_score
from utils.security import get_formatted_certificate_chain_async, get_ssl_checks_async
from . import performance
from . import wordcloud
from . import crawler
from models.analysis import (
    Analysis,
    Check,
    ErrorResult,
    SecurityAndServer,
    Score,
    SeoFiles,
    SeoResult,
    SslCertificate,
    SslCertificatesAndChecks,
    SslChecks,
)


async def analyze(url: str) -> Analysis:
    domain = urlparse(url).netloc
    async with httpx.AsyncClient(
        http2=True, follow_redirects=True, timeout=30
    ) as client:
        visited = set()
        results = []
        all_unsafe_links = set()
        await crawler.crawl(url, domain, client, results, visited, all_unsafe_links)
        favicon_result = await check_if_favicon_is_present(url, client)

        try:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            canonical_url = crawler.check_canonical_tag(soup)
            structured_data = crawler.check_structured_data(soup)
            charset = crawler.check_charset(soup)
            doctype = crawler.check_doctype(response.text)
            metadata_result = await crawler.check_metadata(soup)
            socials_result = await crawler.check_for_social_media_meta_tags(soup)
            search_preview_result = await crawler.get_serch_preview(
                url,
                soup,
                metadata_result.title,
                metadata_result.description,
                favicon_result.found,
            )

        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

        robots_result = await check_file_exists(url, "robots.txt", client)
        sitemap_result = await check_file_exists(url, "sitemap.xml", client)

        wordcloud_result = await wordcloud.create_word_cloud(url, client)
        keywords_distribution = await wordcloud.get_distribution_of_keywords(
            url, client
        )
        performance_result = await performance.check_performance_metrics(url, client)
        spf_record = await crawler.check_spf_record(domain)
        http2_support_result = await crawler.check_http2_support(url, client)
        cert_chain = await get_formatted_certificate_chain_async(domain)
        ssl_checks = await get_ssl_checks_async(domain)
        seo = SeoResult(
            seo_files=SeoFiles(
                robots=robots_result, sitemap=sitemap_result, favicon=favicon_result
            ),
            metadata=metadata_result,
            socials=socials_result,
            search_preview=search_preview_result,
            canonical_url=canonical_url,
            structured_data=structured_data,
            charset=charset,
            doctype=doctype,
        )
        security = SecurityAndServer(
                ssl_certificates=SslCertificatesAndChecks(
                    server_certificate=SslCertificate(
                        **cert_chain["server_certificate"]
                    ),
                    intermediate_certificates=[
                        SslCertificate(**c)
                        for c in cert_chain["intermediate_certificates"]
                    ],
                    root_certificate=SslCertificate(**cert_chain["root_certificate"]),
                    checks=SslChecks(**ssl_checks["checks"]),
                ),
                spf_record=spf_record,
                all_unsafe_links=list(all_unsafe_links),
                http2_support=http2_support_result
            )
        seo_score = get_seo_score(seo, results)
        performance_score = get_performance_score(performance_result)
        security_score = get_security_score(security)
        return Analysis(
            seo=seo,
            wordcloud=wordcloud_result,
            keywords_distribution=keywords_distribution,
            performance=performance_result,
            page_report=results,
            security=security,
            score=Score(seo=seo_score, performance=performance_score, security=security_score),
        )


async def check_file_exists(
    url: str, filename: str, client: httpx.AsyncClient
) -> Union[Check, ErrorResult]:
    file_url = f"{url.rstrip('/')}/{filename}"
    try:
        response = await client.get(file_url)
        found = response.status_code == 200
        return Check(
            found=found,
            status_code=response.status_code,
            file_extension=None,
            message=f"{filename} {'found' if found else 'not found'}",
        )
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))


async def check_if_favicon_is_present(
    url: str, client: httpx.AsyncClient
) -> Union[Check, ErrorResult]:
    favicon_extensions = ["ico", "png", "svg"]
    url = url.rstrip("/")
    for ext in favicon_extensions:
        favicon_url = f"{url}/favicon.{ext}"
        try:
            response = await client.get(favicon_url)
            if response.status_code == 200:
                return Check(
                    found=True,
                    status_code=response.status_code,
                    file_extension=ext,
                    message=f"favicon.{ext} found",
                )
        except httpx.RequestError as e:
            return ErrorResult(error=str(e))

    return Check(found=False, status_code=None, message="No favicon found")
