from pytest import raises
from pydantic import ValidationError
from extractor.models.Article import Article, Author, Citation, PageRange
from extractor.models.Journal import Journal


class TestArticleClass:
    title = "Highly accurate protein structure prediction with AlphaFold"
    publication_year = 2021
    author_list = [("John", "Jumper"), ("Richard", "Evans"), ("Alexander", "Pritzel")]
    authors = [Author(first_name=fname, last_name=last_name) for fname, last_name in author_list]
    journal = Journal.NATURE
    doi = "10.1038/s41586-021-03819-2"
    volume = 596
    issue = None
    pages = PageRange(start=583, end=589)
    open_access = True
    citation = Citation(
        title=title,
        open_access=open_access,
        publication_year=publication_year,
        authors=authors,
        journal=journal,
        doi=doi,
        volume=volume,
        issue=issue,
        pages=pages
    )
    abstract = "This is a synthesis of the entire article content."
    download_url = "https://www.downloadurl.com/download/article"
    figures = [f"https://www.figure.com/fig/{i}" for i in range(3)]
    references = [f"references {i}" for i in range(1,4)]

    def test_complete_fields(self):
        article = Article.model_validate({
            "title": self.title,
            "open_access": self.open_access,
            "citation": self.citation,
            "abstract": self.abstract,
            "download_url": self.download_url,
            "figures": self.figures,
            "references": self.references
        })
        assert len(article.model_fields_set) == 7

    def test_incomplete_fields(self):
        """
        Expect to throw an error if Article does not have the following attributes:
          > title
          > open_access
          > citation
          > abstract
        """
        data = {
            "title": self.title,
            "open_access": self.open_access,
            "citation": self.citation,
            "abstract": self.abstract,
        }
        for reqf in data.keys():
            inc_data = data.copy()
            inc_data.pop(reqf)
            with raises(ValidationError) as excinfo:
                Article.model_validate(inc_data)
            assert excinfo.type == ValidationError
