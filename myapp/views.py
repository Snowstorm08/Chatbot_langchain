from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import json
import logging
from run_model import generate_response, model, tokenizer

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
@csrf_protect  # Use proper CSRF protection in production
def chat_view(request: HttpRequest):
    """
    Chat endpoint for handling LLM interactions.
    Supports:
        - GET  -> Render frontend page
        - POST -> Process chat message
    """

    if request.method == "GET":
        return render(request, "index.html")

    # POST request handling
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON payload."},
            status=400
        )

    message = data.get("message")

    if not message or not isinstance(message, str):
        return JsonResponse(
            {"error": "Message must be a non-empty string."},
            status=400
        )

    if len(message) > 5000:  # Prevent abuse
        return JsonResponse(
            {"error": "Message too long."},
            status=400
        )

    try:
        response_text = generate_response(model, tokenizer, message)

        return JsonResponse(
            {
                "message": response_text
            },
            status=200
        )

    except Exception as e:
        logger.exception("LLM processing failed")

        return JsonResponse(
            {"error": "Internal server error."},
            status=500
        )
