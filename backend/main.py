import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from agents.finder import finder_agent
from base_models.paper import PaperSearchResult

logger = logging.getLogger(__name__)


class SearchRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)

    @field_validator("topic")
    @classmethod
    def topic_must_not_be_blank(cls, value: str) -> str:
        topic = value.strip()
        if len(topic) < 2:
            raise ValueError("Topic must contain at least two characters")
        return topic


def get_allowed_origins() -> list[str]:
    configured_origins = os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]


app = FastAPI(
    title="Papertrail API",
    description="HTTP API for the arXiv paper finder agent.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def run_search_agent(topic: str) -> PaperSearchResult:
    result = finder_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": topic},
            ]
        }
    )
    structured_result = result.get("structured_response")
    if structured_result is None:
        raise RuntimeError("The finder agent returned no structured response")
    return PaperSearchResult.model_validate(structured_result)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search", response_model=PaperSearchResult)
def search_papers(request: SearchRequest) -> PaperSearchResult:
    try:
        return run_search_agent(request.topic)
    except Exception as error:
        logger.exception("Paper search failed for topic %r", request.topic)
        raise HTTPException(
            status_code=502,
            detail="The research agent could not complete this search. Please try again.",
        ) from error
