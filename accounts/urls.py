from django.urls import path
from django.contrib.auth import views

from accounts.views import RegisterView


## aqui sao as urls de login,cadastro e logout aqui que aponta a rota/urls.
urlpatterns=[
    path('accounts/register/',RegisterView.as_view(),name='register'),
    path('accounts/login/',views.LoginView.as_view(),name='login'),
    path('accounts/logout/',views.LogoutView.as_view(),name='logout'),

]
