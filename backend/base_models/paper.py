from pydantic import BaseModel, Field

class Paper(BaseModel):
    arxiv_id: str = Field(description="The arxiv id of the paper")
    title: str = Field(description="The title of the paper")
    authors: list | None = Field(None, description="The authors of the paper")
    publication_date: str | None = Field(None, description="The publication date of the paper")
    abstract: str = Field(description="The abstract of the paper")
    url: str = Field(description="The url of the paper")
    pdf_url: str = Field(description="The pdf url of the paper")
    doi: str | None = Field(None, description="The doi of the paper")
    summary: str | None = Field(None, description="The summary of the paper")

class PaperSearchResult(BaseModel):
    topic: str = Field(description="User topic search")
    papers: list[Paper] | None = Field(None, description="List of papers")

