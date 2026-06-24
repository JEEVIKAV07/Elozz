from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []
embeddings = []


def create_embeddings(pdf_pages):

    global chunks
    global embeddings

    chunks = []

    for page_data in pdf_pages:

        page_number = page_data["page"]
        text = page_data["text"]

        for i in range(0, len(text), 500):

            chunk = text[i:i+500]

            chunks.append({
                "page": page_number,
                "text": chunk
            })

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)


def search_chunks(query, top_k=3):

    global chunks
    global embeddings

    if len(chunks) == 0:
        return []

    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in top_indices:

        results.append({
            "page": chunks[idx]["page"],
            "text": chunks[idx]["text"]
        })

    return results