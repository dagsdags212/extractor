import argparse

from bs4 import BeautifulSoup
import httpx

from extractor.Parser import Parser
from extractor.helpers import classify_url_by_journal, validate_url
from extractor.selectors import TREES

ap = argparse.ArgumentParser(
    prog="extractor",
    description="a CLI tool for extracting article metadata from supported journals",
    epilog="@Jan Samson"
)

ap.add_argument("url", help="article URL")
ap.add_argument("--abstract", help="display article abstract", action="store_true")
ap.add_argument("--references", help="display ALL references used in the article", action="store_true")
ap.add_argument("--authors", help="display ALL authors of the article", action="store_true")

args = ap.parse_args()

def main() -> None:
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

if __name__ == "__main__":
    main()
