from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page view that allows both authenticated and anonymous users"""
    return render(request, 'pages/home.html')

def browser(request):
    return render(request, 'pages/browser.html')

def map(request):
    return render(request, 'pages/map.html')

@login_required
def shelf_saved(request):
    books = request.user.profile.shelves.get(shelf_type='SAVED').books.all()
    return render(request, 'pages/shelf_saved.html', {'books': books})

@login_required
def shelf_borrowed(request):
    books = request.user.profile.shelves.get(shelf_type='BORROWED').books.all()
    return render(request, 'pages/shelf_borrowed.html', {'books': books})

@login_required
def shelf_purchased(request):
    books = request.user.profile.shelves.get(shelf_type='PURCHASED').books.all()
    return render(request, 'pages/shelf_purchased.html', {'books': books})