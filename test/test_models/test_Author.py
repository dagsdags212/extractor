from pydantic import ValidationError
from pytest import raises
from extractor.models.Article import Author


def test_complete_fields():
    author = Author(first_name="John", last_name="Doe", affiliation="foo")
    assert author.model_fields_set == {"first_name", "last_name", "affiliation"}

def test_empty_first_name():
    author = Author(last_name="Doe", affiliation="foo")
    assert author.first_name == ""
    assert author.model_fields_set == {"last_name", "affiliation"}

def test_empty_last_name():
    with raises(ValidationError) as excinfo:
        Author(first_name="John", affiliation="foo")
    assert excinfo.type is ValidationError

def test_empty_affiliation():
    author = Author(first_name="John", last_name="Doe")
    assert author.affiliation == ""
    assert author.model_fields_set == {"first_name", "last_name"}
