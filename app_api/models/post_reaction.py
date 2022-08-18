from django.db import models
from django.contrib.auth.models import User


class PostReaction(models.Model):
    reaction = models.ForeignKey(
        "Reaction", on_delete=models.CASCADE, related_name="post_reactions")
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="post_reactions")
