import json
from pathlib import Path

from app.models.library_page import LibraryPage


class JsonLoader:
    """
    Loads library page records from JSON files.
    """

    @staticmethod
    def load_pages(
        file_path: str | Path,
    ) -> list[LibraryPage]:

        path = Path(file_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        # The sample you provided is a single
        # Elasticsearch document.
        if isinstance(data, dict):
            records = [data]
        else:
            records = data

        pages = []

        for record in records:
            source = record.get(
                "_source",
                record,
            )

            book = source.get(
                "book",
                {},
            )

            language = book.get(
                "language",
                {},
            )

            page = LibraryPage(
                id=source["id"],
                source_id=source["source_id"],
                book_id=source["book_id"],
                section_id=source.get("section_id"),
                content=source["content"],
                page_num=source.get("page_num"),
                image_path=source.get("image_path"),

                title=book.get("title"),
                author=book.get("author"),
                publisher=book.get("publisher"),
                isbn=book.get("isbn"),
                year=book.get("year"),

                language_id=language.get("id"),
                language=language.get("name"),
            )

            pages.append(page)

        return pages
