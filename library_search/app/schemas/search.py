from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SearchResult(BaseModel):
    page_id: int
    book_id: int
    page_num: int
    title: str
    content: str
    score: float | None = None


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]