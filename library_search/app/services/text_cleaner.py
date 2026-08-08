from bs4 import BeautifulSoup


class TextCleaner:

    @staticmethod
    def clean_html(text: str) -> str:
        """
        Convert HTML content into clean plain text.
        """

        if not text:
            return ""

        soup = BeautifulSoup(
            text,
            "html.parser",
        )

        # Extract readable text.
        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        # Normalize excessive blank lines.
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)