from lib.model_client import ModelClientError, generate_answer
from lib.prompt_builder import build_rag_prompt
from lib.response_formatter import (
    format_fallback_response,
    format_sources,
    format_success_response,
)
from lib.retrieval import DEFAULT_TOP_K, retrieve_context


def answer_question(
    question,
    retriever=None,
    prompt_builder=None,
    model_client=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the full RAG workflow for a validated question."""
    # Use provided dependencies when passed, otherwise use default helpers.
    retriever = retriever or retrieve_context            # Real Chroma retrieval by default
    prompt_builder = prompt_builder or build_rag_prompt  # Real prompt builder by default
    model_client = model_client or generate_answer       # Real Ollama call by default
    
    # Retrieve context before building the prompt.
    context_chunks = retriever(question, top_k=top_k)  # Get relevant chunks from Chroma

    # Return fallback response and do not call the model when context is empty.
    if not context_chunks:                             # Nothing relevant was found
        return format_fallback_response(question)      # Safe answer, empty sources; model never called

    # Build the prompt.
    prompt = prompt_builder(question, context_chunks)  # Question + context = full prompt text

    # Call the model client.
    answer = model_client(prompt)  # Send the prompt, get the model's answer back

    # Raise ModelClientError if the model answer is blank or unusable.
    if not isinstance(answer, str) or not answer.strip():  # Not text, or only whitespace
        raise ModelClientError("Model returned an empty answer.")
    
    # Return formatted success response with answer and sources.
    sources = format_sources(context_chunks)  # Trim chunks down to source info
    return format_success_response(answer, sources)  # {"answer": ..., "sources": [...]}