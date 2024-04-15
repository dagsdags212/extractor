import sys
from bs4 import BeautifulSoup
from extractor.models.Article import Article, Author, Citation
from extractor.models.Journal import Journal
from extractor.selectors import TREES


class Parser:
    """
    A helper class containing methods for parsing article fields from different journals.
    """
    @classmethod
    def _extract_text(cls, node) -> str:
        """Extracts the text from an HTML tag stored as a node."""
        if isinstance(node, list):
            return node[0].text
        return node.text

    @classmethod
    def nature_article(cls, html: str) -> Article:
        """Parses an article published in Nature."""
        soup = BeautifulSoup(html, "html.parser")
        tree = TREES["nature"]

        # check if article is open access
        identifiers = soup.select("article header ul.c-article-identifiers li")
        open_access = len(identifiers) == 3

        citation_data = {
            "title": None,
            "publication_year": None,
            "journal": Journal.NATURE,
            "authors": [],
            "volume": None, 
            "issue": None,
            "doi": None,
            }
        # check if title field is provided
        title_node = soup.select(tree.title)
        if title_node:
            citation_data["title"] = Parser._extract_text(title_node)
        # check if publication_year is provided
        publication_year_node = soup.select(tree.publication_year)
        if publication_year_node:
            citation_data["publication_year"] = Parser._extract_text(publication_year_node)
        # check if doi field is provided
        doi_node = soup.select(tree.doi)
        if doi_node:
            citation_data["doi"] = Parser._extract_text(doi_node)
        # parse list of authors
        for node in soup.select(tree.authors)[0]:
            res = node.find("a")
            if res:
                full_name = res.text.split(" ")
                if len(full_name) == 3:
                    first_name, _, last_name = full_name
                elif len(full_name) == 2:
                    first_name, last_name = full_name
                else:
                    continue
                author = Author(first_name=first_name, last_name=last_name)
                citation_data["authors"].append(author)
        # check if volume field is provided
        volume_node = soup.select(tree.volume)
        if volume_node:
            citation_data["volume"] = Parser._extract_text(volume_node)[-2:]
                # check if article number/issue is provided
        issue_node = soup.select(tree.issue)
        if issue_node:
            citation_data["issue"] = issue_node[0].text
        # stores fields in Citation object
        citation = Citation.model_validate(citation_data)

        if not open_access:
            print("\nArticle is not open access. The following fields cannot be accessed:\n")
            for field in ["download_url", "figures", "references"]:
                print(f"> {field}")

        article_data = {
            "title": citation_data["title"],
            "open_access": open_access,
            "citation": citation,
            "abstract": "",
            "download_url": None,
            "figures": [],
            "references": [],
        }
        # extract article fields
        abstract_node = soup.select(tree.abstract)
        if abstract_node:
            article_data["abstract"] = Parser._extract_text(abstract_node)
        if open_access:
            download_url_node = soup.select(tree.download_url)
            if download_url_node:
                article_data["download_url"] = "https://www.nature.com" + download_url_node[0].get("href")
            for node in soup.select(tree.references)[0]:
                res = node.find("p")
                if res:
                    article_data["references"].append(res.text)
            for node in soup.select(tree.figures):
                img = node.find("img")
                if img:
                    article_data["figures"].append(f"https://{img.get("src")[2:]}")
        article = Article.model_validate(article_data)

        return article
