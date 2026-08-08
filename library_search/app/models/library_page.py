from pydantic import BaseModel, Field


class LibraryPage(BaseModel):
    """
    Represents one library page.

    One LibraryPage corresponds to one RAG chunk.
    """

    page_id: int = Field(alias="id")
    source_id: int
    book_id: int
    section_id: int | None = None

    content: str
    page_num: int | None = None
    image_path: str | None = None

    # Book metadata
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    isbn: str | None = None
    year: str | None = None
    language_id: int | None = None
    language: str | None = None

    model_config = {
        "populate_by_name": True,
    }
