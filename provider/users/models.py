from pyexpat import model
from django.contrib.auth.models import User
from django.db import models



class Post(models.Model):
    title= models.CharField(max_length=100)
    body = models.TextField()
    # timestamp = models.DateTimeField(auto_now_add=True)
    # autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
