from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag
from extractor.models.Article import Article, Author, Citation
from extractor.models.Journal import Journal
from extractor.selectors import SelectorTree

class AbstractParser(ABC):
    """A blueprint for writing article-specific parsers.

    The following methods must be implemented by subclasses:
        1. _extract_citation_fields
        2. _extract_article_fields
    """

    def __init__(self, html_str: str, journal: Journal) -> None:
        assert isinstance(html_str, str), f"`html_str` must be of type str, not {type(html_str)}"
        assert isinstance(journal, Journal), f"`journal` must be of type Journal, not {type(journal)}"     
        self._html_str = html_str
        self._journal = journal
        self._soup = self._generate_soup(html_str)
        self._tree = self._identify_selector_tree(journal)

    @property
    def html_str(self) -> str:
        """Getter function for html_str attribute."""
        return self._html_str

    @property
    def journal(self) -> Journal:
        """Getter function for journal attribute."""
        return self._journal

    @property
    def soup(self) -> BeautifulSoup:
        """Getter function for soup attribute."""
        return self._soup

    @property
    def tree(self) -> SelectorTree:
        """Getter function for tree attribute."""
        return self._tree

    def _extract_text(self, tag: Tag | list[Tag]) -> str:
        """Extracts the text from an html tag."""
        if isinstance(tag, list):
            return tag[0].text.strip()
        return tag.text.strip()

    def _identify_selector_tree(self, journal: Journal) -> SelectorTree:
        """Returns a SelectorTree object based on the given journal."""
        # to avoid circular imports
        from extractor.selectors import TREES
        return TREES[journal]

    def _generate_soup(self, html_str: str) -> BeautifulSoup:
        """Parses an HTML string into a BeautifulSoup object."""
        soup = BeautifulSoup(html_str, "html.parser")
        return soup

    @abstractmethod
    def _extract_citation_fields(self) -> dict:
        """A parsing function for extracting citation fields."""

    @abstractmethod
    def _extract_article_fields(self) -> dict:
        """A parsing function for extracting article fields."""

    def generate_article(self) -> Article:
        """Invokes the extraction functions to return an Article object."""
        citation_data = self._extract_citation_fields()
        # create Citation object
        citation = Citation.model_validate(citation_data)
        article_data = self._extract_article_fields()
        article_data.update({"citation": citation})
        article_data.update({"title": citation.title})
        # create and return Article object
        article = Article.model_validate(article_data)
        return article


class NatureParser(AbstractParser):
    """Parser for articles published in Nature."""
    def __init__(self, html_str: str) -> None:
        super().__init__(html_str, Journal.NATURE)

    def _extract_citation_fields(self) -> dict:
        soup, tree = self.soup, self.tree
        # intialize citation_data dictionary
        citation_data = {
            f: None for f in ["title", "publication_year", "volume", "issue", "doi"]
        }
        citation_data["journal"] = self.journal
        citation_data["authors"] = []
        # try to extract node for each selector in the tree
        title_node = soup.select(tree.title)
        publication_year_node = soup.select(tree.publication_year)
        doi_node = soup.select(tree.doi)
        volume_node = soup.select(tree.volume)
        issue_node = soup.select(tree.issue)
        # add checks if extracted nodes are present
        if title_node:
            citation_data["title"] = self._extract_text(title_node)
        if publication_year_node:
            citation_data["publication_year"] = self._extract_text(publication_year_node)
        if doi_node:
            citation_data["doi"] = self._extract_text(doi_node)
        if volume_node:
            citation_data["volume"] = self._extract_text(volume_node)[-2:]
        if issue_node:
            citation_data["issue"] = issue_node[0].text
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

        return citation_data

    def _extract_article_fields(self) -> dict:
        root_url = "https://www.nature.com"
        soup, tree = self.soup, self.tree
        identifiers = soup.select("article header ul.c-article-identifiers li")
        open_access = len(identifiers) == 3

        article_data = {
            "open_access": open_access,
            "abstract": "",
            "download_url": None,
            "figures": [],
            "references": [],
        }
        # extract article fields
        abstract_node = soup.select(tree.abstract)
        if abstract_node:
            article_data["abstract"] = self._extract_text(abstract_node)
        if open_access:
            download_url_node = soup.select(tree.download_url)
            if download_url_node:
                article_data["download_url"] = root_url + download_url_node[0].get("href")
            for node in soup.select(tree.references)[0]:
                res = node.find("p")
                if res:
                    article_data["references"].append(res.text)
            for node in soup.select(tree.figures):
                img = node.find("img")
                if img:
                    article_data["figures"].append(f"https://{img.get("src")[2:]}")

        if not open_access:
            print("\nArticle is not open access. The following fields cannot be accessed:\n")
            for field in ["download_url", "figures", "references"]:
                print(f"> {field}")

        return article_data
