from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f' {self.email}'




class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Contact, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat between {self.owner} and {self.target} '




class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.ForeignKey(Contact , null=True,blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=250)

    def __str__(self):
        return f' [{self.sender}] [{self.receiver}] {self.content} '
