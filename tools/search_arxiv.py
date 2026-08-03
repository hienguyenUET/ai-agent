import arxiv
from langchain.tools import tool

@tool
def search_arxiv(query: str, max_results: int = 5) -> list[dict]:

    """Search arXiv for research papers related to a query."""
    client = arxiv.Client()
    search = arxiv.Search(
      query=query,
      max_results=max_results,
      sort_by=arxiv.SortCriterion.Relevance,
    )

    return [
      {
          "arxiv_id": result.get_short_id(),
          "title": result.title,
          "authors": [author.name for author in result.authors],
          "publication_date": result.published.isoformat(),
          "abstract": result.summary,
          "url": result.entry_id,
          "pdf_url": result.pdf_url,
          "doi": result.doi,
      } for result in client.results(search)
    ]


