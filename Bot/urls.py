from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('input_msg/', views.input_msg, name='input_msg'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
]