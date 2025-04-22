from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(
             template_name='pages/home.html',
             next_page='/'
         ), 
         name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url='/accounts/password-change/done/'
         ),
         name='password_change'
    ),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ),
         name='password_change_done'
    ),
    path('settings/', views.settings_view, name='settings'),
]