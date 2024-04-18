import asyncio
import httpx
from rich.console import Console
from rich.table import Table, Column
from extractor.parsers import NatureParser
from extractor.cli import get_cli_args
from extractor.helpers import classify_url_by_journal, download_article, download_figures, validate_url


def main() -> None:
    # initialize console
    console = Console()

    # extract CLI arguments as Namespace object
    args = get_cli_args()

    # validate url string and send request to fetch article data
    url_string = args.url
    url = validate_url(url_string)
    url = classify_url_by_journal(url)
    client = httpx.Client(follow_redirects=True)
    r = client.get(url, timeout=5.0)
    r.raise_for_status()

    # parser response text an store as an Article object
    article = NatureParser(r.text).generate_article()

    # display article info
    if args.info:
        print(article)

    # display abstract
    if args.abstract:
        print("\n")
        console.print(article.abstract, style="cyan", justify="left")
        print("\n")

    # display list of used references
    if args.references:
        ref_table = Table(
            Column(header="No.", justify="center"),
            Column(header="Citation", justify="left"),
            title="References",
        )
        for i, ref in enumerate(article.references):
            ref_table.add_row(str(i+1), ref)
        console.print(ref_table)

    # display article title
    if args.title:
        print(f"\n{article.title}\n")

    # display list of authors
    if args.authors:
        authors_table = Table(
            Column(header="No.", justify="center"),
            Column(header="Name", justify="center"),
            title="Authors",
        )
        for i, author in enumerate(article.citation.authors):
            authors_table.add_row(str(i+1), str(author))
        console.print(authors_table)

    # download article to default article directory
    if args.download:
        if not article.open_access:
            print("Article is not open access, cannot download.")
        output = download_article(article, client)
        print(f"Article downloaded at {output}")

    # download all figures to default figures directory
    if args.figures:
        figures = asyncio.run(download_figures(article))
        print("\n")
        for i, fig_path in enumerate(figures):
            print(f"Figure {i+1} saved at {fig_path}")

if __name__ == "__main__":
    asyncio.run(main())
