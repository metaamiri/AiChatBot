from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import time
import cohere
import json
from . import bot

def index(request):
    return render(request, 'Bot/index.html')


# Simulated AI response stream (replace with real API)
def ai_stream(message):
    api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
    co = cohere.ClientV2(api_key)

    if not api_key:
        return("Error: Please Configure The API Key.")

    model_name = "command-a-03-2025"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    if not message:
        return "Input cannot be empty."

    conversation.append({"role": "user", "content": message})
    
    response_stream = co.chat_stream(
        model=model_name,
        messages=conversation)
    
    assistant_response = ""

    for chunk in response_stream:
        if chunk.type == "content-delta":
            token_text = chunk.delta.message.content.text
            assistant_response += token_text
            
            yield token_text
            # time.sleep(0.1)  # simulate delay
            
    conversation.append({"role": "assistant", "content": assistant_response})


@csrf_exempt
def input_msg(request):
    message = request.GET.get('message', '')

    def event_stream():
        for chunk in ai_stream(message):
            yield f"data: {chunk}\n\n"  # SSE format

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Needed for some reverse proxies like Nginx
    return response
