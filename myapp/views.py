from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
import logging

from run_model import generate_response, model, tokenizer

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def chat_view(request):
    """
    Chat API endpoint for LLM interaction.
    """

    # -----------------------------------------------------
    # GET Request
    # -----------------------------------------------------
    if request.method == "GET":
        return render(request, "index.html")

    # -----------------------------------------------------
    # POST Request
    # -----------------------------------------------------
    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON payload",
            },
            status=400,
        )

    # -----------------------------------------------------
    # Validate Input
    # -----------------------------------------------------
    message = data.get("message")

    if not message:
        return JsonResponse(
            {
                "success": False,
                "error": "Message is required",
            },
            status=400,
        )

    if not isinstance(message, str):
        return JsonResponse(
            {
                "success": False,
                "error": "Message must be a string",
            },
            status=400,
        )

    message = message.strip()

    if len(message) > 5000:
        return JsonResponse(
            {
                "success": False,
                "error": "Message too long",
            },
            status=400,
        )

    # -----------------------------------------------------
    # Generate Response
    # -----------------------------------------------------
    try:
        response_text = generate_response(
            model=model,
            tokenizer=tokenizer,
            prompt=message,
        )

        return JsonResponse(
            {
                "success": True,
                "message": response_text,
            }
        )

    except Exception as e:
        logger.exception("LLM generation failed")

        return JsonResponse(
            {
                "success": False,
                "error": "Internal server error",
            },
            status=500,
        )
