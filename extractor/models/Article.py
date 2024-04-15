from typing import List, Optional
from pydantic import BaseModel, Field
from extractor.models.Journal import Journal


class Author(BaseModel):
    """Stores author-related information."""
    last_name: str
    first_name: Optional[str]   = Field(default="")
    affiliation: Optional[str]  = Field(default="")

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

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
    open_access: bool
    abstract: str
    references: List[str]
    citation: Optional[Citation]    = Field(default=None)
    download_url: Optional[str]     = Field(default=None)
    figures: Optional[List[str]]    = Field(default=None)

    def __str__(self) -> str:
        f = ""
        f += f"\ntitle            : {self.title}"
        f += f"\nopen access      : {self.open_access}"
        f += f"\nauthor count     : {len(self.citation.authors)}"
        if self.open_access:
            f += f"\ndownload_url     : {self.download_url}"
            f += f"\nreference count  : {len(self.references)}"
            f += f"\nfigure count     : {len(self.figures)}"
        f += "\n"
        return f


