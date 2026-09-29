from flask import Flask, jsonify, request  #(provided)

from lib.model_client import ModelClientError  # Step 5: model client
from lib.rag_service import answer_question  # Step 7: RAG service
from lib.response_formatter import format_error_response  # Step 6: response formatting
from lib.validation import validate_question_payload  # Step 2: request validation


def create_app():
    app = Flask(__name__)

    @app.post("/api/ask")
    def ask():
        # Read the JSON request body.
        payload = request.get_json(silent=True)  # Parsed JSON body, or None if missing/invalid

        # Validate the payload.
        question, error = validate_question_payload(payload)  # (Step 2)

        # Return a 400 JSON response for invalid input.
        if error:
            return jsonify(error), 400  # Error dict as JSON, with "Bad Request" status
        
        # Call answer_question(question) for valid input.
        try:
            result = answer_question(question)  # Run the full RAG workflow (Step 7)
        
        # Return a 502 JSON response for ModelClientError.
        except ModelClientError as error:
            return jsonify(
                format_error_response("model_service_error", str(error))  # example: "Ollama unavailable"
            ), 502  # "Bad Gateway": the service we are depending on failed

        # Return the RAG result as JSON with a 200 status code.
        return jsonify(result), 200  # Success or fallback response

    return app


app = create_app()