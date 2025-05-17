import pytest
from httpx import AsyncClient
from main import app, strip_url
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_analyze_code_endpoint(mocker):
    mock_response = {"mocked": "result"}
    mocker.patch("seo.utils.operations.analyze", return_value=mock_response)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/seo/analyze", json={"url": "https://example.com"})
        assert response.status_code == 200
        assert response.json() == mock_response


def test_strip_url_valid():
    assert strip_url("https://example.com/page") == "https://example.com"


def test_strip_url_invalid():
    with pytest.raises(ValueError):
        strip_url("not_a_url")
