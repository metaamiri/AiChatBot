from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('input_msg/', views.input_msg, name='input_msg'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
]