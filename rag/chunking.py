def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks for retrieval-friendly indexing."""
    chunks = []
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        # Keep a fixed-size window; the final chunk may be shorter.
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Overlap preserves context continuity between neighboring chunks.
        start += (chunk_size - overlap)

    return chunks