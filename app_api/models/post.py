from django.db import models


class Post(models.Model):

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=30)
    publication_date = models.DateField()
    image_url = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    content = models.CharField(max_length=100)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="posts")
    reactions = models.ManyToManyField("Reaction", through="PostReaction", related_name="posts")