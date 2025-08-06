from django.urls import path
from . import views


# urls de chatbot o app.
urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('send_message/', views.chat_send_message, name='chat_send_message'),  
]
