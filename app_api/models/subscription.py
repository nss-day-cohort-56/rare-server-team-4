from django.db import models

class Subscription(models.Model):
    subscriber = models.ForeignKey('RareUser', related_name= 'subscriber', on_delete=models.CASCADE)
    author = models.ForeignKey('RareUser', related_name= 'author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)