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
        print("in register func")
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
            print("User created:", user)
            user.save()
            login(request, user)  # Log the user in after registration
            request.session['user_id'] = user.id  # Store user ID in session 

            return JsonResponse({'status': 'success', 'message': 'Registered successful.'})
        
        
        except IntegrityError as e:
            return JsonResponse({'status': 'error', 'message': 'Username or email already exists.'})
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'})
    
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
    conversation.append({
        "role": "assistant",
        "content": respond
    })
    
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
        conversation_id = data.get('conversation_id','')
        user_msg = data.get('user_msg','')
        bot_msg = data.get('bot_msg','')
        if conversation_id != "":
            conversation = Chat.objects.get(id=conversation_id, user=request.user, title='Conversation')
        else:
            conversation = Chat.objects.create(user=request.user, title='Conversation1')

        Chat.objects.create(chat=conversation, role='user', content=user_msg)
        Chat.objects.create(chat=conversation, role='bot', content=bot_msg)

        conversation.save()
        print("Conversation saved successfully.")
        return JsonResponse({'status': 'success', 'message': 'Conversation saved successfully.', 'conversation_id': conversation.id})
        
    else:
        return JsonResponse({'status':'error','message':'Invalid request method.'})
    

@login_required
def get_user_chats(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    data = [{"id": c.id, "title": c.title} for c in chats]
    return JsonResponse(data, safe=False) 


@login_required
def get_chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Chat not found'})

    messages = chat.messages.order_by('created_date').values('role', 'content', 'created_date')
    return JsonResponse(list(messages), safe=False)

