from extractor.Parser import Parser


def test_nature_article():
    """Expect to return an Article objects from a Nature URL."""
    # this is a valid open-access Nature article
    url = "https://www.nature.com/articles/s41586-021-03819-2#citeas" 
