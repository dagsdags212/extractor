from pytest import raises
from httpx import URL
from extractor.errors import InvalidURLError
from extractor.helpers import validate_url


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


