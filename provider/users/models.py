from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title

class Image(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.caption