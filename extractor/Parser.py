from bs4 import BeautifulSoup
from extractor.models.Article import Article, Author, Citation
from extractor.models.Journal import Journal
from extractor.selectors import TREES


class Parser:
    """
    A helper class containing methods for parsing article fields from different journals.
    """
    def nature_article(html: str) -> Article:
        """Parses an article published in Nature."""
        soup = BeautifulSoup(html, "html.parser")
        tree = TREES["nature"]
        citation_data = {
            "title": soup.select(tree.title)[0].text,
            "publication_year": soup.select(tree.publication_year)[0].text,
            "journal": Journal.NATURE,
            "authors": [],
            "volume": soup.select(tree.volume)[0].text[-2:],
            "issue": soup.select(tree.issue)[0].text,
            "doi": soup.select(tree.doi)[0].text,
        }
        for node in soup.select(tree.authors)[0]:
            res = node.find("a")
            if res:
                first_name, last_name = res.text.split(" ")
                author = Author(first_name=first_name, last_name=last_name)
                citation_data["authors"].append(author)
        citation = Citation.model_validate(citation_data)

        article_data = {
            "title": citation_data["title"],
            "citation": citation,
            "abstract": soup.select(tree.abstract)[0].text,
            "download_url": soup.select(tree.download_url)[0].get("href"),
            "figures": [],
            "references": [],
        }
        for node in soup.select(tree.references)[0]:
            res = node.find("p")
            if res:
                article_data["references"].append(res.text)
        for node in soup.select(tree.figures):
            img = node.find("img")
            if img:
                article_data["figures"].append(img.get("src")[2:])
        article = Article.model_validate(article_data)

        return article
