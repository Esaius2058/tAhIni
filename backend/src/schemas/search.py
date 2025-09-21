from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    top_n: int = 5

class SearchResponse(BaseModel):
    id: str
    text: str
    tags: list[str] | None = None
