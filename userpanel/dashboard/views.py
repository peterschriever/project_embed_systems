from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render

# Create your views here.
@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {"jsFile": "charts.js"})

@ensure_csrf_cookie
def settings(request):
    return render(request, 'settings.html', {"jsFile": "settings.js"})
