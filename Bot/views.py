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


@csrf_exempt
def input_msg(request):
    message = request.GET.get('message', '')

    # Load conversation from session, or initialize it
    conversation = request.session.get('conversation', [])
    
    # Add system prompt only if it's a new conversation
    if not conversation:
        conversation.append({
            "role": "system",
            "content": "You are a helpful assistant."
        })

    # Append user message to conversation
    conversation.append({
        "role": "user",
        "content": message
    })

    # Save updated conversation back to session
    request.session['conversation'] = conversation

    def ai_stream():
        api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
        co = cohere.ClientV2(api_key)
        model_name = "c4ai-aya-expanse-32b"

        response_stream = co.chat_stream(
            model=model_name,
            messages=conversation
        )

        for chunk in response_stream:
            if chunk.type == "content-delta":
                token_text = chunk.delta.message.content.text
                yield f"data: {token_text}\n\n"  # SSE format

        yield f"data: __end__ \n\n"
        

    return StreamingHttpResponse(ai_stream(), content_type='text/event-stream')


def save_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        assistant_response = data.get('assistant_response', '')
        if not assistant_response:
            return JsonResponse({'status':'error','message': 'No conversation to save.'})
        try:
            conversation = request.session.get('conversation', [])
            conversation.append({"role": "assistant","content": assistant_response})
            request.session['conversation'] = conversation  # Ensure session is updated

            return JsonResponse({'status': 'success', 'message': 'Conversation saved successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error saving conversation: {str(e)}'})
    
    else:
        return JsonResponse({'status':'error','message':'Invalid request method.'})