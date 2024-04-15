from pathlib import Path
import httpx
import pytest
from extractor.Parser import Parser
from extractor.helpers import classify_url_by_journal, download_article, validate_url
from extractor.models.Journal import Journal


@pytest.mark.asyncio
async def test_valid_response():
    url_str = "https://www.nature.com/articles/s41586-021-03819-2#citeas"
    url = validate_url(url_str)
    url = classify_url_by_journal(url)
    with httpx.Client() as client:
        r = client.get(url, follow_redirects=True)
    article = Parser.nature_article(r.text)
    download_path = download_article(article, client)
    client.close()
    assert url.journal == Journal.NATURE
    assert r.status_code <= 200
    assert isinstance(download_path, Path)
