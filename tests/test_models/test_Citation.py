from pytest import raises
from pydantic import ValidationError
from extractor.models.Journal import Journal
from extractor.models.Article import Author, PageRange, Citation


class TestCitationClass:
    title = "Highly accurate protein structure prediction with AlphaFold"
    publication_year = 2021
    author_list = [("John", "Jumper"), ("Richard", "Evans"), ("Alexander", "Pritzel")]
    authors = [Author(first_name=fname, last_name=last_name) for fname, last_name in author_list]
    journal = Journal.NATURE
    doi = "10.1038/s41586-021-03819-2"
    volume = 596
    issue = None
    pages = PageRange(start=583, end=589)

    def test_complete_fields(self):
        data = {
            "title": self.title,
            "publication_year": self.publication_year,
            "authors": self.authors,
            "journal": self.journal,
            "volume": self.volume,
            "issue": self.issue,
            "doi": self.doi,
            "pages": self.pages, 
        }
        citation = Citation.model_validate(data)
        assert len(citation.model_fields_set) == 8

    def test_required_fields(self):
        data = {
            "title": self.title,
            "publication_year": self.publication_year,
            "authors": self.authors,
            "journal": self.journal,
        }
        citation = Citation.model_validate(data)
        assert len(citation.model_fields_set) == 4
        for reqf in data.keys():
            incomplete_data = data.copy()
            incomplete_data.pop(reqf)
            with raises(ValidationError) as excinfo:
                Citation.model_validate(incomplete_data)
            assert excinfo.type == ValidationError

    def test_optional_fields(self):
        data = {
            "title": self.title,
            "publication_year": self.publication_year,
            "authors": self.authors,
            "journal": self.journal,
            "volume": self.volume,
            "issue": self.issue,
            "doi": self.doi,
            "pages": self.pages, 
        }
        optional_fields = ["volume", "issue", "doi", "pages"]
        for optf in optional_fields:
            incomplete_data = data.copy()
            incomplete_data.pop(optf)
            citation = Citation.model_validate(incomplete_data)
            assert len(citation.model_fields_set) == 7
