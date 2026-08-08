from app.database.weaviate_client import client
from app.services.embedding_service import EmbeddingService
from app.services.weaviate_service import WeaviateService


def main():
    try:
        # -------------------------------------------------
        # 1. Initialize services
        # -------------------------------------------------

        embedding_service = EmbeddingService()
        weaviate_service = WeaviateService(client)

        print("Services initialized.")

        # -------------------------------------------------
        # 2. Create collection
        # -------------------------------------------------

        weaviate_service.create_collection()

        print("LibraryPage collection is ready.")

        # -------------------------------------------------
        # 3. Test page
        # -------------------------------------------------

        page = {
            "page_id": 1,
            "book_id": 100,
            "section_id": 10,
            "page_num": 1,
            "content": (
                "این یک صفحه آزمایشی از کتاب است. "
                "این کتاب درباره تاریخ و فرهنگ ایران صحبت می‌کند."
            ),
            "title": "کتاب آزمایشی",
            "author": "نویسنده آزمایشی",
            "publisher": "ناشر آزمایشی",
            "language": "فارسی",
        }

        # -------------------------------------------------
        # 4. Generate document embedding
        # -------------------------------------------------

        print("Generating document embedding...")

        vector = embedding_service.embed_document(
            page["content"]
        )

        print(
            f"Embedding dimension: {len(vector)}"
        )

        # -------------------------------------------------
        # 5. Insert
        # -------------------------------------------------

        object_id = weaviate_service.insert(
            page=page,
            vector=vector,
        )

        print(
            f"Document inserted with UUID: {object_id}"
        )

        # -------------------------------------------------
        # 6. Query embedding
        # -------------------------------------------------

        query = "این کتاب درباره چه موضوعی است؟"

        print(f"Query: {query}")

        query_vector = embedding_service.embed_query(
            query
        )

        print(
            f"Query embedding dimension: "
            f"{len(query_vector)}"
        )

        # -------------------------------------------------
        # 7. Search
        # -------------------------------------------------

        print("\n--- Vector Search ---")

        results = weaviate_service.search(
            vector=query_vector,
            limit=3,
        )

        # -------------------------------------------------
        # 8. Display results
        # -------------------------------------------------

        print(f"Found {len(results)} result(s).")

        for result in results:
            print(f"Page ID  : {result['page_id']}")
            print(f"Book ID  : {result['book_id']}")
            print(f"Page Num : {result['page_num']}")
            print(f"Title    : {result['title']}")
            print(f"Content  : {result['content']}")
            print(f"Distance : {result['distance']}")
            print("-" * 50)

    except Exception as e:
        print("\n!!! ERROR !!!")
        print(type(e).__name__)
        print(e)

        raise

    finally:
        client.close()
        print("\nWeaviate client closed.")


if __name__ == "__main__":
    main()