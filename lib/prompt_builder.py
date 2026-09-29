def format_context_chunk(chunk):
    """Format one retrieved chunk for the prompt context block."""
    # Include source_id, title, category, section, and text.
    return (
        f"[Source: {chunk.get('source_id')}]\n"   # Source ID the model can cite
        f"Title: {chunk.get('title')}\n"          # Document title
        f"Category: {chunk.get('category')}\n"    # ex: Billing
        f"Section: {chunk.get('section')}\n"      # Section within the document
        f"Text: {chunk.get('text')}"              # The actual policy text
    )


def build_rag_prompt(question, context_chunks):
    """Build a structured RAG prompt from a question and retrieved context."""
    # TODO: Validate that the question is not blank.
    # TODO: Validate that context_chunks contains usable text.
    # TODO: Build a prompt with these sections:
    #       Instructions:
    #       Context:
    #       Question:
    #       Response Requirements:
    # TODO: Tell the model to use only approved context and avoid unsupported claims.
    raise NotImplementedError("Implement build_rag_prompt().")