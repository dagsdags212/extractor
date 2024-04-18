from extractor.models.Journal import Journal


class SelectorTree:
    """
    Base class for creating selector trees.
    A tree is a mapping of field information to its selector path.

    Usage
    ================
    article_tree = {
        "root": "html",
        "title": "head title",
        "authors": "div span.author",
    }
    parser = SelectorTree(article_tree)
    """
    def __init__(self, tree: dict[str, str]) -> None:
        for node, path in tree.items():
            setattr(self, node, path)

NATURE_SELECTORS = {
    "title": "article header h1[data-test='article-title']",
    "publication_year": "p.c-article-info-details > span[data-test='article-publication-year']",
    "abstract": "div.c-article-body section[data-title='Abstract'] p",
    "volume": "article header p.c-article-info-details b[data-test='journal-volume']",
    "issue": "article header p.c-article-info-details span[data-test='article-number']",
    "download_url": "aside div.c-pdf-download a",
    "doi": "span.c-bibliographic-information__value:nth-child(3)",
    "references": "div#Bib1-content div[data-container-section='references'] ol",
    "authors": "article header ul[data-test='authors-list']",
    "figures": "div[data-test='figure'] figure",
}

PLOS_SELECTORS = {
    "title": "div.title-authors h1#artTitle",
    "publication_year": "div.article-title-etc ul.date-doi li#artPubDate",
    "abstract": "div#artText div.abstract div.abstract-content p",
    "volume": "div.article-content div.articleinfo:nth-child(1)",
    "issue": "div.article-content div.articleinfo:nth-child(1)",
    "download_url": "aside div.dload-menu div.dload-pdf a",
    "doi": "div.article-title-etc ul.date-doi li#artDoi a",
    "references": "ol.references",
    "authors": "div.title-authors ul"
}


TREES = {
    Journal.NATURE: SelectorTree(NATURE_SELECTORS),
}
