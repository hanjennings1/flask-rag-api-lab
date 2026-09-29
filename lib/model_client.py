import requests

DEFAULT_MODEL_NAME = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"


class ModelClientError(Exception):
    """Raised when the local model service cannot return a usable answer."""

def generate_answer(prompt, model_name=DEFAULT_MODEL_NAME, base_url=DEFAULT_BASE_URL):
    """Send the prompt to a local Ollama model and return the generated answer."""
    # Validate that prompt is a non-empty string.
    if not isinstance(prompt, str) or not prompt.strip():  # Not text, or only whitespace
        raise ModelClientError("Prompt must be a non-empty string.")
    
    # POST to {base_url}/api/generate.
    url = f"{base_url}/api/generate"

    # Send model, prompt, and stream=False as JSON.
    payload = {                # The JSON body Ollama expects
        "model": model_name,   # Which model to use, e.g. llama3.2
        "prompt": prompt,      # The full RAG prompt
        "stream": False,       # Return the whole answer at once, not word by word
    }

    # Use a timeout.
    try:
        response = requests.post(url, json=payload, timeout=60)  # Send the request/give up after 60 seconds
        response.raise_for_status()                              # Turn HTTP error codes into exceptions

    # Raise ModelClientError for request failures, bad JSON, or missing response.
    except requests.RequestException as error:  # Any network or HTTP failure
        raise ModelClientError(f"Model request failed: {error}") from error
    
    # Return the stripped response text.
    try:
        data = response.json()      # Parse the JSON body into a Python dict
    except ValueError as error:     # Body wasn't valid JSON
        raise ModelClientError("Model returned invalid JSON.") from error

    answer = data.get("response") if isinstance(data, dict) else None   # The generated text, if present

    if not isinstance(answer, str) or not answer.strip():               # Missing, not text, or blank
        raise ModelClientError("Model response was missing or empty.")

    return answer.strip()       # Clean answer text