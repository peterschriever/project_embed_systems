from django.shortcuts import render

# Create your views here.
def templateFunction(request):
    for key,val in request.POST.items():
        #do stuff
        print(key+":"+val)
    return render(request, 'index.html', {"asd": True})