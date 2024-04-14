from httpx import URL
from extractor.errors import InvalidURLError
from extractor.models.Journal import Journal


def validate_url(url_string: str) -> URL:
    """
    Validates the components of the url string.
    If valid, returns a URL object. Otherwise, raises an error.
    """
    try:
        url = URL(url_string)
        # warn user if url is using an unsecure scheme
        if url.scheme != "https":
            print("URL is using an unsecure scheme")
        # a valid URL must at least have a host and path
        if url.host and url.path:
            return url
        raise InvalidURLError("URL must have a scheme, host, and path to be valid")
    except TypeError as err:
        raise err

def classify_url_by_journal(url: URL) -> URL:
    """Identifies the journal from the URL host."""
    for journal in Journal:
        if journal in url.host:
            url.journal = journal
            return url
    print("Journal not found from URL host")
    url.journal = None
    return url
