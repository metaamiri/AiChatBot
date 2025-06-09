from django.shortcuts import render

def index(request):

    return render(request, 'Bot/index.html')

