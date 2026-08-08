from pathlib import Path

from app.database.weaviate_client import client
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.json_loader import JsonLoader
from app.services.weaviate_service import WeaviateService


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DATA_FILE = Path(
    "data/pages.json"
)

BATCH_SIZE = 32


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
        # 2. Create collection
        # -------------------------------------------------

        weaviate_service.create_collection()

        print(
            "LibraryPage collection is ready."
        )

        # -------------------------------------------------
        # 3. Load JSON
        # -------------------------------------------------

        print(
            f"\nLoading data from: {DATA_FILE}"
        )

        pages = JsonLoader.load_pages(
            DATA_FILE
        )

        total_pages = len(pages)

        print(
            f"Loaded {total_pages} pages."
        )

        if total_pages == 0:
            print("Nothing to ingest.")
            return

        # -------------------------------------------------
        # 4. Process batches
        # -------------------------------------------------

        total_ingested = 0

        for start in range(
            0,
            total_pages,
            BATCH_SIZE,
        ):

            end = min(
                start + BATCH_SIZE,
                total_pages,
            )

            batch = pages[start:end]

            print(
                f"\nProcessing pages "
                f"{start + 1}-{end} "
                f"of {total_pages}..."
            )

            try:

                ingested = (
                    ingestion_service.ingest_pages(
                        batch
                    )
                )

                total_ingested += ingested

                print(
                    f"Batch completed: "
                    f"{ingested} pages."
                )

                print(
                    f"Progress: "
                    f"{end}/{total_pages}"
                )

            except Exception as e:

                print(
                    f"\nERROR processing batch "
                    f"{start + 1}-{end}"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

                # Stop ingestion rather than silently
                # losing a batch.
                raise

        # -------------------------------------------------
        # 5. Summary
        # -------------------------------------------------

        print("\n" + "=" * 50)

        print(
            "INGESTION COMPLETED"
        )

        print(
            f"Total pages: {total_pages}"
        )

        print(
            f"Successfully ingested: "
            f"{total_ingested}"
        )

        print("=" * 50)

    finally:

        client.close()

        print(
            "\nWeaviate client closed."
        )


if __name__ == "__main__":
    main()