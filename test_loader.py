from app.injestion.loader import load_pdfs_from_folder


folder = r"C:\Users\hp\Desktop\project\data"

documents = load_pdfs_from_folder(folder)


for document in documents:
    print("File:", document["file_name"])
    print(document["text"][:500])
    print("-" * 50)