from django.shortcuts import render
from . import bot

def index(request):

    return render(request, 'Bot/index.html')

def input_msg(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        if not user_input:
            return render(request, 'Bot/index.html', {'error': 'Input cannot be empty.'})


        # bot.main(user_input)  Call the bot's main function with user input
        response = "API is working fine, your input was: " + user_input

        if not response:
            return render(request, 'Bot/index.html', {'error': 'No response generated.'})

        return render(request, 'Bot/index.html', {'response': response})

