from pinecone import Pinecone, ServerlessSpec

from app.config.settings import settings


pc = Pinecone(
    api_key=settings.pinecone_api_key
)


def create_index():

    index_name = settings.pinecone_index_name

    existing_indexes = pc.list_indexes().names()

    if index_name not in existing_indexes:

        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print(f"Index '{index_name}' created.")

    else:

        print(f"Index '{index_name}' already exists.")


def get_index():

    return pc.Index(
        settings.pinecone_index_name
    )