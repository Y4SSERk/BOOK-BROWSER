from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'pages/home.html')
    # return HttpResponse("<h1>Welcome to the Book API</h1>")

@login_required
def browser(request):
    return render(request, 'pages/browser.html')
    # return HttpResponse("<h1>Welcome to the Book Browser</h1>")

@login_required
def map(request):
    return render(request, 'pages/map.html')
    # return HttpResponse("<h1>Welcome to the Book Map</h1>")

