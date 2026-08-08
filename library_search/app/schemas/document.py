from pydantic import BaseModel, Field


class LibraryPage(BaseModel):
    page_id: int
    book_id: int
    page_num: int
    title: str
    content: str = Field(..., min_length=1)


class DocumentResponse(BaseModel):
    page_id: int
    uuid: str


class BatchDocumentRequest(BaseModel):
    documents: list[LibraryPage]


class BatchDocumentResponse(BaseModel):
    inserted: int
    failed: int
    uuids: list[str]