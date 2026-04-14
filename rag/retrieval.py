from backend.embedding.specter_embedding import get_embedding

def retrieve_chunks(vector_store, query,k=5):
    """Embed a query and return nearest chunks from the vector index."""
    # Query and document chunks must share the same embedding space.
    query_vec = get_embedding(query)
    return vector_store.search(query_vec,k)