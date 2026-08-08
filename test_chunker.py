from app.injestion.loader import load_pdfs_from_folder
from app.injestion.chunker import chunk_text


folder = r"C:\Users\hp\Desktop\project\data"

documents = load_pdfs_from_folder(folder)


for document in documents:

    chunks = chunk_text(document["text"])

    print("File:", document["file_name"])
    print("Number of chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i + 1}:")
        print(chunk[:500])

    print("-" * 70)