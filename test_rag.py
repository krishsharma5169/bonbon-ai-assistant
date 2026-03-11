from backend.app.rag.embedder import get_embedding 
from backend.app.rag.vectorstore import search 
q = get_embedding('given an array of integers find all pairs that sum to a target value') 
hits = search(q, n_results=3) 
for h in hits: print(h['score'], h['metadata']['topic']) 
