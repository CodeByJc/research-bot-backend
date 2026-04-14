import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        """Initialize an in-memory FAISS L2 index and chunk lookup table."""
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add(self, embeddings, chunks):
        """Add embedding vectors and keep aligned source chunks for retrieval."""
        self.index.add(np.array(embeddings))
        self.chunks.extend(chunks)

    def search(self, query_vec, k=5):
        """Return top-k text chunks nearest to the query vector."""
        # FAISS returns neighbor indexes; map them back to original chunk text.
        D, I = self.index.search(np.array([query_vec]), k)
        return [self.chunks[i] for i in I[0]]