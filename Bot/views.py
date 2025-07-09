from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login, logout  # Import the login function
from django.contrib.auth.decorators import login_required
from . import bot
from .models import *
from langdetect import detect
import time
import markdown2
import cohere
import json


@login_required(login_url='/signin/')
def index(request):
    return render(request, 'Bot/index.html', {"user":request.user})

def signin(request):
    # Render the signin page
    return render(request, 'Bot/signin.html')

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')

        # Simple validation
        if not username or not email or not password:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        # Here you would typically save the user to the database
        # For now, we just return a success message
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            login(request, user)  # Log the user in after registration
            request.session['user_id'] = user.id  # Store user ID in session 

            return JsonResponse({'status': 'success', 'message': 'Registered successful.'})
        
        except User.IntegrityError as e:
            if 'unique constraint' in str(e):
                return JsonResponse({'status': 'error', 'message': 'Username or email already exists.'})
            else:
                return JsonResponse({'status': 'error', 'message': f'Error creating user: {str(e)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def login_view(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        # Simple validation
        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Username and password are required.'})
        
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                login(request, user)  # Django's built-in login function
                request.session['user_id'] = user.id  # Store user ID in session

                return JsonResponse({'status': 'success', 'message': 'Login successful.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Password is incorrect.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist.'})
        

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})  

def logout_view(request):
    logout(request)  # Log out the user
    return HttpResponseRedirect(reverse("signin"))  # Redirect to signin page


@csrf_exempt
@login_required(login_url='/signin/')
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
    
    api_key = "VDnP5YX4y3nC2V0ala8GrzUtX2CdKPn0mLGGr3Yq"
    co = cohere.ClientV2(api_key)
    model_name = "command-a-03-2025"

    response_stream = co.chat(
        model=model_name,
        messages=conversation
    )
    respond = response_stream.message.content[0].text
    
    if detect(respond) in ["fa","ar"]:
        dir = "rtl"
    else:   
        dir = "ltr"
        
    return JsonResponse({'message':response_stream.message.content[0].text, "dir":dir, "status":"success"}, safe=False)

    # def ai_stream():
    #     try:
    #         buffer = ""
    #         converted = ""
    #         for chunk in response_stream:
    #             if chunk.type == "content-delta":
    #                 token_text = chunk.delta.message.content.text
    #                 buffer += token_text
    #                 # converted = markdown2.markdown(buffer)  # Convert Markdown to HTML
    #                 print(token_text, end="", flush=True)
    #                 yield f"data: {token_text}\n\n"  # SSE format

    #     except Exception as e:
    #         yield f"data: Error: {str(e)}\n\n"
    #     # yield f"data: __end__ \n\n"
        

    # response = StreamingHttpResponse(ai_stream(), content_type="text/event-stream; charset=utf-8")
    # response["Cache-Control"] = "no-cache"
    # return response


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
            print("Conversation saved:", conversation)
            return JsonResponse({'status': 'success', 'message': 'Conversation saved successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error saving conversation: {str(e)}'})
    
    else:
        return JsonResponse({'status':'error','message':'Invalid request method.'})