# from app.services.embedding_service import EmbeddingService


# embedding_service = EmbeddingService()


# text = "FastAPI is a Python web framework."

# vector = embedding_service.embed(text)


# print(len(vector))
# print(vector[:5])
#----------------------------------------------------------------

from app.services.embedding_service import EmbeddingService


embedding_service = EmbeddingService()

document = "FastAPI is a Python web framework."
query = "What is FastAPI?"

document_vector = embedding_service.embed_document(document)
query_vector = embedding_service.embed_query(query)

print("Dimension:", embedding_service.dimension)
print("Document vector length:", len(document_vector))
print("Query vector length:", len(query_vector))
print("First 5 values:", query_vector[:5])