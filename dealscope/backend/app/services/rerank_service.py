from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_chunks(
    query: str,
    chunks:list,
    top_k: int = 5,
):
    
    if not chunks:
        return[]
    
    pairs = [
        (query , chunk["content"])
        for chunk in chunks
    ]
    
    scores = model.predict(pairs)
    
    ranked_chunks = []
    
    for chunk, score in zip(chunks , scores):
        chunk = dict(chunk)
        chunk["rerank_score"]=float(score)
        ranked_chunks.append(chunk)
        
    ranked_chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True,
    )
    
    return ranked_chunks[:top_k]