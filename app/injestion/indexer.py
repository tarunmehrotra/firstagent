from app.injestion.loader import load_pdfs_from_folder
from app.injestion.chunker import chunk_text
from app.injestion.embedder import create_embedding
from app.retrival.pinecone_client import get_index
from app.config.settings import settings


def index_documents(folder_path: str):

    documents = load_pdfs_from_folder(folder_path)

    index = get_index()

    vectors = []

    for document in documents:

        file_name = document["file_name"]
        text = document["text"]

        chunks = chunk_text(text)

        print(f"Processing: {file_name}")
        print(f"Chunks created: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            embedding = create_embedding(chunk)

            vector_id = f"{file_name}-{i}"

            metadata = {
                "file_name": file_name,
                "chunk_id": i,
                "text": chunk
            }

            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })

    if vectors:

        index.upsert(
            vectors=vectors,
            namespace=settings.pinecone_namespace
        )

        print(f"\nSuccessfully uploaded {len(vectors)} vectors to Pinecone.")