from email.policy import default
from enum import unique
from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Grade(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length = 200)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null = True, )

    def __str__(self):
        return self.name



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg" )
    grade= models.ForeignKey(Grade, on_delete= models.SET_NULL, null=True)
    

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = []
        


class Room(models.Model):
    host = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete= models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete= models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User , related_name='participants', blank="True")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']
    #this allows us to render only the first 50 characters of the body
    def __str__(self):

        return self.body[0:50]















