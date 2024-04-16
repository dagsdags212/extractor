from httpx import URL
from extractor.helpers import classify_url_by_journal
from extractor.models.Journal import Journal


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
