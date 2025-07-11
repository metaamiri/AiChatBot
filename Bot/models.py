from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.username}"
    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    ROLE_CHOICES  = [
        ('user', 'user'),
        ('bot', 'bot')
    ]
    role = models.CharField(max_length=4, choices=ROLE_CHOICES)  # 'user' or 'bot'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:20]}..."  # Display first 20 characters
    