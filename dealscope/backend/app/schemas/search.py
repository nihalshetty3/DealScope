from pydantic import BaseModel

class SearchResult(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    page_number: int | None
    distance: float

class SearchResponse(BaseModel):
    results: list[SearchResult]