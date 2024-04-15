import asyncio
import sys
import httpx
from extractor.Parser import Parser
from extractor.cli import get_cli_args
from extractor.helpers import classify_url_by_journal, download_article, download_figures, validate_url


def main() -> None:
    args = get_cli_args()
    url_string = args.url
    url = validate_url(url_string)
    url = classify_url_by_journal(url)
    client = httpx.Client(follow_redirects=True)
    r = client.get(url, timeout=5.0)
    r.raise_for_status()

    article = Parser.nature_article(r.text)

    if args.info:
        print(article)
        sys.exit(0)
    if args.abstract:
        print("\n", article.abstract, "\n")
        sys.exit(0)
    if args.references:
        print("\n")
        for i, ref in enumerate(article.references):
            print(f"[{i+1}] {ref}")
        print("\n")
        sys.exit(0)
    if args.authors:
        print("\n")
        for i, author in enumerate(article.citation.authors):
            print(f"[{i+1}] {author}")
        print("\n")
    if args.download:
        if not article.open_access:
            print("Article is not open access, cannot download.")
            sys.exit(1)
        output = download_article(article, client)
        print(f"Article downloaded at {output}")
    if args.figures:
        figures = asyncio.run(download_figures(article))
        print("\n")
        for i, fig_path in enumerate(figures):
            print(f"Figure {i+1} saved at {fig_path}")

if __name__ == "__main__":
    main()
