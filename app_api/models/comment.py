from django.db import models

# This class is joined by user and posts
class Comment(models.Model):
    author_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=250)