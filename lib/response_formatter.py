FALLBACK_MESSAGE = (
    "The approved customer success documents do not contain enough information "
    "to answer that question. Review the relevant policy or contact a supervisor "
    "before acting on this request."
)


def format_sources(context_chunks):
    """Return source metadata for retrieved context chunks."""
    # Return unique source dictionaries.
    sources = []
    seen_chunk_ids = set()  # Chunk IDs already added, to skip duplicates

    for chunk in context_chunks:
        chunk_id = chunk.get("id")

        if chunk_id in seen_chunk_ids:  # Already added this chunk
            continue
        seen_chunk_ids.add(chunk_id)  # Remember it for next time

    # Include id, title, category, section, and chunk_id.
    # Do not include full text or distance values in source entries.
        sources.append({
            "id": chunk.get("source_id"),     # Document ID, e.g. "SUB-101"
            "title": chunk.get("title"),
            "category": chunk.get("category"),
            "section": chunk.get("section"),
            "chunk_id": chunk_id,             # Which chunk of that document
        })

    return sources


def format_success_response(answer, sources):
    """Return the successful RAG API response body."""
    # Return {"answer": cleaned_answer, "sources": sources_list}.
    return {
        "answer": answer.strip(),     # Clean up any extra spaces around the model's answer
        "sources": list(sources),     # The source entries from format_sources()
    }


def format_fallback_response(question=None):
    """Return a safe response when there is not enough approved context."""
    # Return FALLBACK_MESSAGE with an empty sources list.
    return {
        "answer": FALLBACK_MESSAGE,  # Fixed, safe message (defined at the top of  file)
        "sources": [],               # No sources, since no approved context was used
    }


def format_error_response(error, message):
    """Return a standard error response body."""
    # Return {"error": error, "message": message}.
    return {
        "error": error,
        "message": message,  # Human-readable explanation
    }