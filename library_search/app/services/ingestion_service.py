from app.models.library_page import LibraryPage
from app.services.embedding_service import EmbeddingService
from app.services.text_cleaner import TextCleaner
from app.services.weaviate_service import WeaviateService


class IngestionService:
    """
    Handles the ingestion of library pages into Weaviate.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        weaviate_service: WeaviateService,
    ):
        self.embedding_service = embedding_service
        self.weaviate_service = weaviate_service

    def ingest_page(
        self,
        page: LibraryPage,
    ) -> str:

        # ---------------------------------------------
        # 1. Clean page content
        # ---------------------------------------------

        clean_content = TextCleaner.clean_html(
            page.content
        )

        if not clean_content:
            raise ValueError(
                f"Page {page.page_id} has empty content."
            )

        # ---------------------------------------------
        # 2. Generate embedding
        # ---------------------------------------------

        vector = self.embedding_service.embed_document(
            clean_content
        )

        # ---------------------------------------------
        # 3. Prepare Weaviate data
        # ---------------------------------------------

        weaviate_page = {
            "page_id": page.page_id,
            "book_id": page.book_id,
            "section_id": page.section_id,
            "page_num": page.page_num,
            "content": clean_content,
            "title": page.title,
            "author": page.author,
            "publisher": page.publisher,
            "language": page.language,
        }

        # ---------------------------------------------
        # 4. Store in Weaviate
        # ---------------------------------------------

        return self.weaviate_service.insert(
            page=weaviate_page,
            vector=vector,
        )

    def ingest_pages(
        self,
        pages: list[LibraryPage],
    ) -> int:
        """
        Ingest a batch of library pages.

        Returns the number of successfully prepared pages.
        """

        valid_pages = []
        texts = []

        # -------------------------------------------------
        # 1. Clean pages
        # -------------------------------------------------

        for page in pages:

            clean_content = TextCleaner.clean_html(
                page.content
            )

            if not clean_content:
                print(
                    f"Skipping page {page.page_id}: "
                    "empty content."
                )
                continue

            valid_pages.append(
                (
                    page,
                    clean_content,
                )
            )

            texts.append(clean_content)

        if not texts:
            return 0

        # -------------------------------------------------
        # 2. Generate embeddings in one batch
        # -------------------------------------------------

        vectors = (
            self.embedding_service.embed_documents(
                texts
            )
        )

        # -------------------------------------------------
        # 3. Prepare Weaviate objects
        # -------------------------------------------------

        weaviate_pages = []

        for page, clean_content in valid_pages:

            weaviate_pages.append(
                {
                    "page_id": page.page_id,
                    "book_id": page.book_id,
                    "section_id": page.section_id,
                    "page_num": page.page_num,
                    "content": clean_content,
                    "title": page.title,
                    "author": page.author,
                    "publisher": page.publisher,
                    "language": page.language,
                }
            )

        # -------------------------------------------------
        # 4. Batch insert into Weaviate
        # -------------------------------------------------

        self.weaviate_service.insert_batch(
            pages=weaviate_pages,
            vectors=vectors,
        )

        return len(weaviate_pages)