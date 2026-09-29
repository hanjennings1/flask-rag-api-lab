CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "customer_success_knowledge"
DEFAULT_TOP_K = 3


def get_chroma_collection(path=CHROMA_PATH, collection_name=COLLECTION_NAME):
    """Return a persistent Chroma collection for manual local testing."""
    # Import chromadb inside this function.
    import chromadb

    # Create a PersistentClient using path.
    client = chromadb.PersistentClient(path=path)
    # Return get_or_create_collection(collection_name).
    return client.get_or_create_collection(collection_name)


def format_chroma_results(results):
    """Normalize Chroma query results into context chunk dictionaries.
    Chroma query results often look like:
        {
            "ids": [["chunk-1"]],
            "documents": [["Text"]],
            "metadatas": [[{"source_id": "SRC-1"}]],
            "distances": [[0.12]]
        }
    """
    # Handle nested Chroma result lists.
    ids = (results.get("ids") or [[]])[0]
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    # Skip missing or blank documents.
    chunks = []  # Collects one dictionary per usable chunk

    for index, chunk_id in enumerate(ids):  # index = position, chunk_id = the ID at that position
        text = documents[index] if index < len(documents) else None  # None if no matching document

        if not text or not text.strip():    # Missing, empty, or whitespace-only
            continue                        # Skip this chunk and move to the next one

    # Return dictionaries with id, text, source_id, title, category, section, and distance keys.
        metadata = (metadatas[index] if index < len(metadatas) else None) or {}  # {} if missing or None
        distance = distances[index] if index < len(distances) else None  # None if no distance given
        
        chunks.append({                                  # Add one normalized chunk to the list
            "id": chunk_id,                              # Chunk's unique ID
            "text": text.strip(),                        # Cleaned chunk text
            "source_id": metadata.get("source_id"),      # Policy document ID, ex: "SUB-101"
            "title": metadata.get("title"),              # Document title
            "category": metadata.get("category"),        # ex: "Billing"
            "section": metadata.get("section"),          # Section within the document
            "distance": distance,                        # Similarity score (lower = closer match)
        })
    
    return chunks  # All usable chunks, in Chroma's order


def retrieve_context(question, collection=None, top_k=DEFAULT_TOP_K):
    """Retrieve context chunks for a user question.
    Tests may pass a fake collection. Manual use should call Chroma.
    """
    # Strip the question.
    question = question.strip()  # Remove extra spaces from both ends

    # Use the provided collection or get_chroma_collection().
    if not question:        # Blank question: nothing to search for
        return []           # Return no chunks, without querying Chroma

    if collection is None:  # No collection passed in (normal app use)
        collection = get_chroma_collection()  # Connect to the real Chroma database

    # Call collection.query() with query_texts, n_results, and include.
    results = collection.query(                                 # Ask Chroma for similar chunks
        query_texts=[question],                                 # The question, wrapped in a list
        n_results=top_k,                                        # How many chunks to return
        include=["documents", "metadatas", "distances"],        # What data to send back
    )

    # Return normalized context chunks.
    return format_chroma_results(results)  # Unwrap and regroup into chunk dictionaries