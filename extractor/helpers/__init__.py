import asyncio
from pathlib import Path
import sys
from httpx import URL, AsyncClient, Client, HTTPError
from extractor import DEFAULT_ARTICLE_DIRPATH, DEFAULT_FIGURES_DIRPATH
from extractor.errors import InvalidURLError
from extractor.models.Article import Article
from extractor.models.Journal import Journal


def validate_url(url_string: str) -> URL:
    """
    Validates the components of the url string.
    If valid, returns a URL object. Otherwise, raises an error.
    """
    try:
        url = URL(url_string)
        # warn user if url is using an unsecure scheme
        if url.scheme != "https":
            print("URL is using an unsecure scheme")
        # a valid URL must at least have a host and path
        if url.host and url.path:
            return url
        raise InvalidURLError("URL must have a scheme, host, and path to be valid")
    except TypeError as err:
        raise err

def classify_url_by_journal(url: URL) -> URL:
    """Identifies the journal from the URL host."""
    for journal in Journal:
        if journal in url.host:
            url.journal = journal
            return url
    print("Journal not found from URL host")
    url.journal = None
    return url

def download_article(article: Article, client: Client) -> Path:
    """Fetches url from the `download_url` attribute and writes binary data to file."""
    try:
        r = client.get(article.download_url, timeout=5.0)
        r.raise_for_status()
        lead_author = article.citation.authors[0].last_name
        filename = f"{lead_author}({article.citation.publication_year}).pdf"
        output_file = DEFAULT_ARTICLE_DIRPATH / filename
        with open(output_file, "wb") as f:
            f.write(r.content)
        f.close()
    except HTTPError as exc:
        print(f"HTTP Exception for {exc.request.url} - {exc}")
        sys.exit(1)
    return output_file

async def save_figure(article: Article, figure_url: str, client: AsyncClient) -> list[Path]:
    try:
        r = await client.get(figure_url)
        filename = figure_url.split("/")[-1]
        lead_author = article.citation.authors[0].last_name
        publication_year = article.citation.publication_year
        dirname = f"{lead_author}({publication_year})"
        dirpath = DEFAULT_FIGURES_DIRPATH / dirname
        if not dirpath.is_dir():
            dirpath.mkdir()
        output_file = dirpath / filename
        with open(output_file, "wb") as f:
            f.write(r.content)
        f.close()
    except HTTPError as exc:
        print(f"HTTP Exception for {exc.request.url} - {exc}")
        sys.exit(1)
    return output_file

async def download_figures(article: Article) -> list[Path]:
    """Fetches a list of urls stored in the article's `figure` attribute."""
    async with AsyncClient() as client:
        figures = await asyncio.gather(
            *[save_figure(article, url, client) for url in article.figures]
        )
    return figures
