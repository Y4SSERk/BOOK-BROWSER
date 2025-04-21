from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User

class SignUpView(CreateView):
    model = User
    template_name = 'accounts/signup.html'  # Correct template path
    fields = ('username', 'email', 'password')
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

@login_required
def profile_view(request):
    shelves = request.user.profile.shelves.all()
    return render(request, 'accounts/profile.html', {
        'shelves': shelves
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('/')  # Direct redirect to home
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')
