# app/database/weaviate_client.py
import weaviate
from app.services.embedding_service import EmbeddingService
from app.services.weaviate_service import WeaviateService

# Weaviate client — shared across all routes
client = weaviate.connect_to_local()

# Shared service singletons — model loaded once
embedding_service = EmbeddingService()
weaviate_service  = WeaviateService(client=client)