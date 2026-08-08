from pathlib import Path

from app.database.weaviate_client import client
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.json_loader import JsonLoader
from app.services.weaviate_service import WeaviateService


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

# Change this to the location of your JSON file.
DATA_FILE = Path("C:/Users/Partiran/Desktop/Semantic Search/ghaemieh_DB/page_record_example2.json")


def main():
    try:
        # -------------------------------------------------
        # 1. Initialize services
        # -------------------------------------------------

        print("Initializing services...")

        embedding_service = EmbeddingService()

        weaviate_service = WeaviateService(
            client
        )

        ingestion_service = IngestionService(
            embedding_service=embedding_service,
            weaviate_service=weaviate_service,
        )

        print("Services initialized.")

        # -------------------------------------------------
        # 2. Make sure Weaviate collection exists
        # -------------------------------------------------

        print("Creating/checking Weaviate collection...")

        # weaviate_service.delete_collection()
        weaviate_service.create_collection()

        print("LibraryPage collection is ready.")

        # -------------------------------------------------
        # 3. Load pages from JSON
        # -------------------------------------------------

        print(
            f"\nLoading pages from: {DATA_FILE}"
        )

        pages = JsonLoader.load_pages(
            DATA_FILE
        )

        print(
            f"Loaded {len(pages)} page(s)."
        )

        if not pages:
            print("No pages found.")
            return

        # -------------------------------------------------
        # 4. Show first page
        # -------------------------------------------------

        page = pages[0]

        print("\n--- First Page ---")
        print(f"Page ID  : {page.page_id}")
        print(f"Book ID  : {page.book_id}")
        print(f"Section  : {page.section_id}")
        print(f"Page Num : {page.page_num}")
        print(f"Title    : {page.title}")
        print(f"Author   : {page.author}")
        print(f"Publisher: {page.publisher}")
        print(f"Language : {page.language}")

        print("\nOriginal content:")
        print(page.content[:500])

        # -------------------------------------------------
        # 5. Ingest only the first page
        # -------------------------------------------------

        print(
            "\nIngesting first page..."
        )

        object_id = ingestion_service.ingest_page(
            page
        )

        print(
            f"\nPage successfully inserted!"
        )

        print(
            f"Weaviate UUID: {object_id}"
        )

        # -------------------------------------------------
        # 6. Test retrieval
        # -------------------------------------------------

        print(
            "\nTesting vector search..."
        )

        query = "این کتاب درباره چیست؟"

        query_vector = (
            embedding_service.embed_query(
                query
            )
        )

        results = weaviate_service.search(
            vector=query_vector,
            limit=3,
        )

        print(
            f"\nFound {len(results)} result(s)."
        )

        for index, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"\n--- Result {index} ---"
            )

            print(
                f"Page ID  : {result['page_id']}"
            )

            print(
                f"Book ID  : {result['book_id']}"
            )

            print(
                f"Page Num : {result['page_num']}"
            )

            print(
                f"Title    : {result['title']}"
            )

            print(
                f"Distance : {result['distance']}"
            )

            print(
                f"Content  : "
                f"{result['content'][:500]}"
            )

    except Exception as e:

        print("\n!!! ERROR !!!")
        print(
            f"Type: {type(e).__name__}"
        )
        print(
            f"Message: {e}"
        )

        raise

    finally:

        # -------------------------------------------------
        # 7. Close Weaviate
        # -------------------------------------------------

        client.close()

        print(
            "\nWeaviate client closed."
        )


if __name__ == "__main__":
    main()