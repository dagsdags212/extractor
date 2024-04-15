import argparse
from bs4 import BeautifulSoup
import httpx
from extractor import DEFAULT_ARTICLE_DIRPATH, DEFAULT_FIGURES_DIRPATH
from extractor.Parser import Parser
from extractor.helpers import classify_url_by_journal, validate_url
from extractor.selectors import TREES
from extractor.cli import cli_args


def main() -> None:
    args = cli_args
    url_string = args.url
    url = validate_url(url_string)
    url = classify_url_by_journal(url)

    client = httpx.Client(follow_redirects=True)
    r = client.get(url, timeout=5.0)
    r.raise_for_status()
    html = r.content

    article = Parser.nature_article(html)

    if args.abstract:
        print("\n", article.abstract, "\n")
    if args.references:
        print("\n")
        for i, ref in enumerate(article.references):
            print(f"[{i+1}] {ref}")
    if args.authors:
        print("\n")
        for i, author in enumerate(article.citation.authors):
            print(f"[{i+1}] {author}")
    if args.dirpaths:
        print("\n")
        print(f"Article directory: {DEFAULT_ARTICLE_DIRPATH}")
        print(f"Figures directory: {DEFAULT_FIGURES_DIRPATH}")

if __name__ == "__main__":
    main()
