# app/api/routes/documents.py
from fastapi import APIRouter, HTTPException

from app.schemas.document import (
    LibraryPage,
    DocumentResponse,
    BatchDocumentRequest,
    BatchDocumentResponse,
)
from app.database.weaviate_client import embedding_service, weaviate_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# -------------------------------------------------
# Create one document
# -------------------------------------------------
@router.post("", response_model=DocumentResponse)
def create_document(page: LibraryPage):
    try:
        embedding = embedding_service.embed_document(page.content)

        uuid = weaviate_service.insert(
            page=page.model_dump(),
            vector=embedding,
        )

        return DocumentResponse(page_id=page.page_id, uuid=str(uuid))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# Batch document insertion
# -------------------------------------------------
@router.post("/batch", response_model=BatchDocumentResponse)
def create_documents_batch(request: BatchDocumentRequest):
    inserted = 0
    failed = 0
    uuids = []

    try:
        texts = [page.content for page in request.documents]
        embeddings = embedding_service.embed_documents(texts)

        for page, embedding in zip(request.documents, embeddings):
            try:
                uuid = weaviate_service.insert(
                    page=page.model_dump(),
                    vector=embedding,
                )
                uuids.append(str(uuid))
                inserted += 1
            except Exception:
                failed += 1

        return BatchDocumentResponse(
            inserted=inserted,
            failed=failed,
            uuids=uuids,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# Get one document
# -------------------------------------------------
@router.get("/{page_id}")
def get_document(page_id: int):
    document = weaviate_service.get_by_page_id(page_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page_id} not found",
        )

    return document


# -------------------------------------------------
# Delete one document
# -------------------------------------------------
@router.delete("/{page_id}")
def delete_document(page_id: int):
    deleted = weaviate_service.delete_by_page_id(page_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page_id} not found",
        )

    return {
        "page_id": page_id,
        "deleted": True,
    }