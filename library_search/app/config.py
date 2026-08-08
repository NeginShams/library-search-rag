from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    embedding_model: str = (
        "jinaai/jina-embeddings-v5-text-nano-retrieval"
    )

    embedding_device: str = "cuda"

    embedding_batch_size: int = 32

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Retrieval
    retrieval_top_k: int = 5
    retrieval_dense_weight: float = 0.4
    retrieval_bm25_weight: float = 0.6


settings = Settings()