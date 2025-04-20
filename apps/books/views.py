from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')
    # return HttpResponse("<h1>Welcome to the Book API</h1>")

def browser(request):
    return render(request, 'pages/browser.html')
    # return HttpResponse("<h1>Welcome to the Book Browser</h1>")

def map(request):
    return render(request, 'pages/map.html')
    # return HttpResponse("<h1>Welcome to the Book Map</h1>")