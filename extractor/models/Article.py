from typing import List, Optional
from pydantic import BaseModel, Field
from extractor.models.Journal import Journal


class Author(BaseModel):
    """Stores author-related information."""
    last_name: str
    first_name: Optional[str]   = Field(default="")
    affiliation: Optional[str]  = Field(default="")

class PageRange(BaseModel):
    """Stores the start and end indices of an article."""
    start: int | str
    end: Optional[int]          = Field(default=None)

class Citation(BaseModel):
    """Stores fields found in an article citation."""
    title: str
    publication_year: int
    authors: List[Author]
    journal: Journal
    volume: Optional[int]       = Field(default=None)
    issue: Optional[int]        = Field(default=None)
    doi: Optional[str]          = Field(default=None)
    pages: Optional[PageRange]  = Field(default=None)

class Article(BaseModel):
    """Stores article-related information."""
    title: str
    citation: Citation
    abstract: str
    download_url: str
    figures: List[str]
    references: List[Citation]