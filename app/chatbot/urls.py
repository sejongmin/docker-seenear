from django.urls import path
from .views import *

urlpatterns = [
    path('chatbot/', chatbot, name='voice-chatbot'),
    # path('endConversation/', views.endConversation, name='endConversation'),
    # path('startConversation/', views.startConversation, name='startConversation'),
    # path('getSummary/', views.getSummary, name='getSummary'),
]