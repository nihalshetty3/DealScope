import fitz

def extract_text_from_pdf(file_path: str) -> list[dict]:
    document = fitz.open(file_path)
    
    pages=[]
    
    for page_number , page in enumerate(document , start=1):
        text = page.get_text("text")
        
        if text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )
    document.close()
    return pages


def chunk_text(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:

    chunks = []

    chunk_idx = 0

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "chunk_index": chunk_idx,
                        "content": chunk,
                        "page_number": page_number
                    }
                )

                chunk_idx += 1

            start += chunk_size - overlap

    return chunks