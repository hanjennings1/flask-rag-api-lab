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
    # Validate that the question is not blank.
    if not question or not question.strip():  # Missing or whitespace-only question
        raise ValueError("Question cannot be blank.")
    
    # Validate that context_chunks contains usable text.
    usable_chunks = []                      # Chunks that actually contain text
    for chunk in context_chunks:
        text = chunk.get("text") or ""      # Use "" if text is missing or None
        if text.strip():                    # Keep only chunks with real text
            usable_chunks.append(chunk)

    if not usable_chunks:                   # Nothing usable to ground the answer in
        raise ValueError("Context must contain at least one chunk with text.")

    question = question.strip()             # Clean the question for the prompt

    # Build a prompt with these sections: Instructions, Context, Question, Response Requirements
    # Format each chunk, separated by a blank line

    context_text = "\n\n".join(format_context_chunk(chunk) for chunk in usable_chunks)

    return (
        # Tell the model to use only approved context and avoid unsupported claims.
        "Instructions:\n"
        "You are a customer success assistant. \n"
        "- Use only the approved context provided below.\n"
        "- Do not invent rules, dates, prices, or exceptions.\n"
        "- If the approved context does not cover part of the question, say so.\n\n"

        "Context:\n"
        f"{context_text}\n\n"

        "Question:\n"
        f"{question}\n\n"

        "Response Requirements:\n"
        "- Answer concisely in plain language that a support representative can use.\n"
        "- Point out any missing information the representative should confirm.\n"
        "- Reference the source ID for each fact you use (for example, SUB-101)."
    )


