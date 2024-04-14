from pytest import raises
from httpx import URL
from extractor.helpers import validate_url, classify_url_by_journal
from extractor.models.Journal import Journal
from extractor.errors import InvalidURLError


class TestValidateUrlFunction:
    """Series of tests for the validate_url function."""
    def test_valid_url(self):
        """Expect to return a http URL object."""
        url_string = "https://www.nature.com/articles/s41421-024-00665-0"
        url = validate_url(url_string)
        assert isinstance(url, URL)

    def test_invalid_url_type(self):
        """Except to raise a TypeError."""
        with raises(TypeError) as excinfo:
            validate_url(13)
        assert excinfo.type == TypeError

    def test_invalid_url_format(self):
        """Expect to raise an InvalidURLError."""
        with raises(InvalidURLError) as excinfo:
            validate_url("/articles/s41421-024-00665-0")
        assert excinfo.type == InvalidURLError

class TestClassifyUrlByJournalFunction:
    """Series of tests for the classify_url_by_journal function."""
    def test_url_with_journal_name(self):
        """Expect URL with journal attribute."""
        u = URL("https://www.nature.com/articles/s41421-024-00665-0")
        url = classify_url_by_journal(u)
        assert isinstance(url.journal, Journal)

    def test_url_without_journal_name(self):
        """Expect URL without journal attribute."""
        u = URL("https://www.nojournal.com/articles/s41421-024-00665-0")
        url = classify_url_by_journal(u)
        assert url.journal is None
