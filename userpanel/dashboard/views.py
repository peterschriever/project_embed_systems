from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {"asd": True})

def settings(request):
    return render(request, 'settings.html', {"asd": False})
