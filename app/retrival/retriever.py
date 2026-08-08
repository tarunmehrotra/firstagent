from app.injestion.embedder import create_embedding
from app.retrival.pinecone_client import get_index
from app.config.settings import settings


def retrieve(query: str, top_k: int = 5):
    # Convert user query into embedding
    query_embedding = create_embedding(query)

    # Get Pinecone index
    index = get_index()

    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=settings.pinecone_namespace
    )

    return results.matches