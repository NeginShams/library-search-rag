from app.config import settings
from app.database.weaviate_client import client
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.weaviate_service import WeaviateService


def main():

    try:
        # =====================================================
        # Configuration
        # =====================================================

        print("=" * 60)
        print("Retrieval Configuration")
        print("=" * 60)

        print(
            f"Top-K              : "
            f"{settings.retrieval_top_k}"
        )

        print(
            f"Dense weight       : "
            f"{settings.retrieval_dense_weight}"
        )

        print(
            f"BM25 weight        : "
            f"{settings.retrieval_bm25_weight}"
        )

        print(
            f"Weaviate alpha     : "
            f"{settings.retrieval_dense_weight}"
        )

        # =====================================================
        # Initialize services
        # =====================================================

        print("\n" + "=" * 60)
        print("Initializing services...")
        print("=" * 60)

        embedding_service = EmbeddingService()

        weaviate_service = WeaviateService(
            client
        )

        retrieval_service = RetrievalService(
            embedding_service=embedding_service,
            weaviate_service=weaviate_service,
        )

        print("Services initialized.")

        # =====================================================
        # Query
        # =====================================================

        query = (
            "این کتاب درباره چه موضوعی است؟"
        )

        print("\n" + "=" * 60)
        print("Query")
        print("=" * 60)

        print(query)

        # =====================================================
        # Hybrid retrieval
        # =====================================================

        print("\n" + "=" * 60)
        print("Running hybrid search...")
        print("=" * 60)

        results = retrieval_service.search(
            query=query
        )

        # =====================================================
        # Results
        # =====================================================

        print("\n" + "=" * 60)
        print(
            f"Retrieved {len(results)} result(s)"
        )
        print("=" * 60)

        if not results:
            print("No results found.")
            return

        for index, result in enumerate(
            results,
            start=1,
        ):

            print(
                f"\n---------- Result {index} ----------"
            )

            print(
                f"UUID     : "
                f"{result.get('uuid')}"
            )

            print(
                f"Page ID  : "
                f"{result.get('page_id')}"
            )

            print(
                f"Book ID  : "
                f"{result.get('book_id')}"
            )

            print(
                f"Page Num : "
                f"{result.get('page_num')}"
            )

            print(
                f"Title    : "
                f"{result.get('title')}"
            )

            print(
                f"Score    : "
                f"{result.get('score')}"
            )

            print(
                f"Explain  : "
                f"{result.get('explain_score')}"
            )
            print(
                f"Content  : "
                f"{result.get('content')}"
            )

    except Exception as e:

        print("\n" + "=" * 60)
        print("Retrieval failed")
        print("=" * 60)

        print(
            f"{type(e).__name__}: {e}"
        )

        raise

    finally:

        client.close()

        print(
            "\nWeaviate client closed."
        )


if __name__ == "__main__":
    main()