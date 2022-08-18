from tkinter import CASCADE
from django.db import models

# This class is joined by user and posts
class Comment(models.Model):
    subject = models.CharField(max_length=250)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created_on = models.DateField()