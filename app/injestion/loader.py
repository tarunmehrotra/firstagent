from pathlib import Path
from pypdf import PdfReader


def load_pdfs_from_folder(folder_path: str):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder.is_dir():
        raise ValueError(f"Path is not a folder: {folder_path}")

    documents = []

    for pdf_file in folder.glob("*.pdf"):

        reader = PdfReader(pdf_file)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        documents.append({
            "file_name": pdf_file.name,
            "file_path": str(pdf_file),
            "text": "\n".join(pages)
        })

    return documents