from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Post
from django.db.models import Q
from app_api.models.user import User


class PostView(ViewSet):
    """post view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            user = user.objects.get(user=request.auth.user)
            # game.is_owner = player.id == game.player.id
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        search_text = self.request.query_params.get('q', None)
        # order_by = self.request.query_params.get('orderby', None)

        posts = Post.objects.all()

        if search_text is not None:
            posts = posts.filter(
                Q(title__contains=search_text)
            )

        category = request.query_params.get('category', None)

        if category is not None:
            posts = posts.filter(category_id=category)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        user = User.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category_id"])

        post = Post.objects.create(
            user=user,
            category=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            content=request.data["content"],
            approved=False
        )

        if request.data["image_url"] is not None:
            post.image_url=request.data["image_url"]
            post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        if user.id != post.user.id:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content','approved')
        depth = 1