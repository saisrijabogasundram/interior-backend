from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from openai import OpenAI

client = None

def get_client():
    global client
    if client is None:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return client

SYSTEM_PROMPT = """You are a helpful interior design assistant for an Indian interior design company.
You help customers with:
- Interior design ideas and inspiration
- Budget estimates for different rooms
- Information about modular kitchens, wardrobes, living rooms, bedrooms
- Booking designers and consultations
- Project timelines and process

Always respond in a friendly, helpful manner. If asked about pricing, give approximate ranges in Indian Rupees.
Keep responses concise and helpful. If user wants to book a designer, tell them to visit /designers page."""

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        openai_client = get_client()  # ✅ ఇలా call చేయి

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
        )

        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
