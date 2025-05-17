import pytest
from unittest.mock import Mock, patch
import asyncio
from urllib.parse import urlparse
from models.analysis import BrokenLink, PageIssues, PageReport, Socials, SearchPreview
from utils.crawler import (
    fetch,
    estimate_image_is_large,
    check_link_status,
    crawl,
    check_metadata,
    check_for_social_media_meta_tags,
    get_serch_preview,
    check_http2_support,
    check_unsafe_cross_origin_links,
    check_canonical_tag,
    check_structured_data,
    check_flash_content,
    check_frameset_usage,
    check_noindex_tag,
    check_spf_record,
    check_doctype,
    check_charset,
    check_deprecated_html,
)

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def mock_soup():
    return Mock()

@pytest.mark.asyncio
async def test_fetch(mock_client):
    mock_response = Mock()
    mock_response.text = "<html></html>"
    mock_client.get.return_value = mock_response  
    url = "http://example.com"
    response = await fetch(mock_client, url)
    assert response == "<html></html>"
    mock_client.get.assert_called_once_with(url, timeout=10)


@pytest.mark.asyncio
async def test_check_link_status(mock_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_client.head.return_value = mock_response  
    
    url = "http://example.com"
    status = await check_link_status(mock_client, url)
    assert status is None

    mock_response.status_code = 404
    status = await check_link_status(mock_client, url)
    assert status == "404 Not Found"


@pytest.mark.asyncio
async def test_crawl(mock_client):
    mock_client.get.return_value.text = "<html><a href='http://example.com/page'></a></html>"
    visited = set()
    results = []
    all_unsafe_links = set()
    domain = "example.com"
    
    await crawl("http://example.com", domain, mock_client, results, visited, all_unsafe_links)
    assert len(results) == 0 

@pytest.mark.asyncio
async def test_check_metadata(mock_soup):
    mock_description_tag = Mock(attrs={"name": "description", "content": "Test Description"})
    mock_soup.find.return_value = mock_description_tag 
    metadata = await check_metadata(mock_soup)
    assert metadata.title is None
    assert metadata.description == "Test Description"


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_check_for_social_media_meta_tags(mock_soup):
    mock_title_tag = Mock(attrs={"property": "og:title", "content": "Test Title"})
    mock_soup.find.return_value = mock_title_tag  
    socials = await check_for_social_media_meta_tags(mock_soup)
    assert socials.title_value == "Test Title"


@pytest.mark.asyncio
async def test_get_serch_preview(mock_soup):
    mock_soup.find_all.return_value = [Mock(string='{"@graph": [{"datePublished": "2021-01-01"}]}')]
    search_preview = await get_serch_preview(
        "http://example.com", mock_soup, "Test Title", "Test Description", True
    )
    assert search_preview.date is not None
    assert search_preview.title == "Test Title"
    assert search_preview.description == "Test Description"

@pytest.mark.asyncio
async def test_check_http2_support(mock_client):
    mock_response = Mock()
    mock_response.http_version = "HTTP/2"
    mock_client.get.return_value = mock_response  
    
    result = await check_http2_support("http://example.com", mock_client)
    assert result is True

    mock_response.http_version = "HTTP/1.1"
    result = await check_http2_support("http://example.com", mock_client)
    assert result is False


def test_estimate_image_is_large():
    img_tag = Mock(attrs={"src": "https://example.com/large-image-1024.jpg"})
    assert estimate_image_is_large(img_tag) is True

    img_tag = Mock(attrs={"src": "https://example.com/small-image.jpg"})
    assert estimate_image_is_large(img_tag) is False

def test_check_unsafe_cross_origin_links(mock_soup):
    mock_a_tag = Mock(href="http://unsafe.com")
    mock_soup.find_all.return_value = [mock_a_tag]  
    unsafe_links = check_unsafe_cross_origin_links(mock_soup, "http://example.com")
    assert "http://unsafe.com" in unsafe_links


def test_check_canonical_tag(mock_soup):
    mock_link_tag = Mock(attrs={"rel": "canonical", "href": "http://example.com"})
    mock_soup.find.return_value = mock_link_tag 
    canonical_url = check_canonical_tag(mock_soup)
    assert canonical_url == "http://example.com"


def test_check_structured_data(mock_soup):
    mock_soup.find_all.return_value = [Mock(get_text=Mock(return_value='{"@type": "Article"}'))]
    structured_data = check_structured_data(mock_soup)
    assert len(structured_data) > 0

def test_check_flash_content(mock_soup):
    mock_soup.find_all.return_value = [Mock(name="object")]
    flash_content = check_flash_content(mock_soup)
    assert flash_content is True

def test_check_frameset_usage(mock_soup):
    mock_soup.find_all.return_value = [Mock(name="frameset")]
    frameset_used = check_frameset_usage(mock_soup)
    assert frameset_used is True

def test_check_noindex_tag(mock_soup):
    mock_meta_tag = Mock(attrs={"name": "robots", "content": "noindex"})
    mock_soup.find.return_value = mock_meta_tag
    noindex_tag = check_noindex_tag(mock_soup)
    assert noindex_tag is True


def test_check_spf_record():
    domain = "example.com"
    with patch("dns.resolver.resolve") as mock_resolve:
        mock_resolve.return_value = [Mock(strings=[b"v=spf1 include:_spf.example.com ~all"])]
        spf_check = asyncio.run(check_spf_record(domain))
        assert spf_check.found is True

def test_check_doctype():
    html_text = "<!doctype html>"
    doctype = check_doctype(html_text)
    assert doctype == "<!doctype html>"

    html_text = "<html>"
    doctype = check_doctype(html_text)
    assert doctype is None

def test_check_charset(mock_soup):
    mock_meta_tag = Mock(attrs={"charset": "UTF-8"})
    mock_soup.find.return_value = mock_meta_tag  
    charset = check_charset(mock_soup)
    assert charset == "UTF-8"


def test_check_deprecated_html(mock_soup):
    mock_soup.find.return_value = Mock(name="font")
    deprecated_tags = check_deprecated_html(mock_soup)
    assert "font" in deprecated_tags
