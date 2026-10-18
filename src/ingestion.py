from pypdf import PdfReader
import chromadb

def extract_and_chunk_pdf(pdf_path:str, chunk_size:int=1000) -> list[str]:
    reader = PdfReader(pdf_path)
    full_text = ""
    for pages in reader.pages:
        page_text = pages.extract_text()
        if page_text:
            full_text+=page_text + "\n"
    chunks = []
    for i in range(0, len(full_text), chunk_size):
        chunks.append(full_text[i:i+chunk_size])
    return chunks
def store_and_retrive_financials(chunks: list[str])->str:
    client = chromadb.Client()
    try:
        client.delete_collection("financial_docs")
    except Exception:
        pass
    collection = client.create_collection(name="financial_docs")
    ids = [f"chunk_{i}"for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)

    results = collection.query(
        query_texts =["Consolidated Balance Sheet Assets Liabilities Debt Equity Income EBIT Revenue"],
        n_results = min(4, len(chunks))
    )
    return "\n----\n".join(results["documents"][0])