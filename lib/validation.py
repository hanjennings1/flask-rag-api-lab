MIN_QUESTION_LENGTH = 3


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    
    # Require payload to be a dictionary.
    if not isinstance(payload, dict):
        return None, {
            "error": "invalid_request",
            "message": "Request body must be a JSON object.",
        }
    
    # Require a question field.
    if "question" not in payload:
        return None, {
            "error": "missing_question",
            "message": "Request body must include a question.",
        }

    # Require question to be a string.
    question = payload["question"]
    if not isinstance(question, str):
        return None, {
            "error": "invalid_question",
            "message": "Question must be a string.",
        }

    # Strip extra whitespace.
    question = question.strip()

    # Reject blank questions.
    if not question:
        return None, {
            "error": "empty_question",
            "message": "Question cannot be blank.",
        }
    # Reject questions shorter than MIN_QUESTION_LENGTH.
    if len(question) < MIN_QUESTION_LENGTH:
        return None, {
            "error": "short_question",
            "message": f"Question must be at least {MIN_QUESTION_LENGTH} characters long.",
        }

    # If passing all of the above:
    return question, None
