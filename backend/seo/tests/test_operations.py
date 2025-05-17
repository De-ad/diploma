import pytest

from models.analysis import Check, ErrorResult, WordCloudResult
from utils import security
from utils import wordcloud
from utils import operations
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, mock_open
from httpx import Response, Request

@pytest.mark.asyncio
async def test_analyze_invalid_url(mocker):
    mock_get = mocker.AsyncMock(side_effect=Exception("Mocked request failure"))
    mocker.patch("seo.utils.operations.httpx.AsyncClient.get", new=mock_get)

    result = await operations.analyze("https://badurl.test")
    assert isinstance(result, ErrorResult)
    assert "Mocked request failure" in result.error


@pytest.mark.asyncio
async def test_create_word_cloud_success():
    html_content = """
        <html><head><title>Test Page</title></head>
        <body><h1>Hello world</h1><p>This is a test test test.</p></body></html>
    """
    mock_response = Response(200, content=html_content.encode("utf-8"))
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("analysis.load_stopwords", return_value={"is", "a", "this"}):
        result = await wordcloud.create_word_cloud("http://example.com", mock_client)

    assert isinstance(result, WordCloudResult)
    words = [item["text"] for item in result.data]
    assert "test" in words
    assert "hello" in words
    assert "world" in words

@pytest.mark.asyncio
async def test_create_word_cloud_failure_status():
    mock_response = Response(404)
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    result = await wordcloud.create_word_cloud("http://example.com", mock_client)
    assert isinstance(result, ErrorResult)
    assert "Status code" in result.error

@pytest.mark.asyncio
async def test_get_distribution_of_keywords():
    html = """
    <html>
        <head><title>Test</title><meta name="description" content="test keyword test" /></head>
        <body><h1>Keyword here</h1><p>test keyword test</p></body>
    </html>
    """
    mock_response = Response(200, content=html.encode("utf-8"))
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("analysis.load_stopwords", return_value={"a", "the", "is"}):
        result = await wordcloud.get_distribution_of_keywords("http://example.com", mock_client, top_n=1)

    assert isinstance(result, dict)
    assert "total" in result
    assert "keyword" in result["total"]

@pytest.mark.asyncio
async def test_check_ssl_certificate_valid():
    with patch("ssl.create_default_context"), patch("socket.socket"):
        result = await security.check_ssl_certificate("example.com")
        assert isinstance(result, Check)
        assert result.status_code == 200

@pytest.mark.asyncio
async def test_get_formatted_certificate_chain_async():
    with patch("analysis.fetch_full_cert_chain_openssl", return_value=[]):
        result = await security.get_formatted_certificate_chain_async("example.com")
        assert isinstance(result, dict)
        assert "server_certificate" in result

@pytest.mark.asyncio
async def test_get_ssl_checks_async():
    mock_result = {
        "checks": {
            "not_used_before_activation_date": True,
            "not_expired": True,
            "hostname_matches": True,
            "trusted_by_major_browsers": True,
            "uses_secure_hash": True,
        }
    }
    with patch("analysis.get_ssl_checks", return_value=mock_result):
        result = await security.get_ssl_checks_async("example.com")
        assert "checks" in result
