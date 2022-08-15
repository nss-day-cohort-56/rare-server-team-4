from django.db import models

class Tag(models.Model):
    """Tag Class"""
    label = models.CharField(max_length=100)
