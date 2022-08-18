from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Post, Category
from django.db.models import Q
from app_api.models import RareUser, Category


class PostView(ViewSet):
    """post view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            user = RareUser.objects.get(user=request.auth.user)
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

        posts = Post.objects.all()

        if search_text is not None:
            posts = posts.filter(
                Q(title__contains=search_text)
            )

        category = request.query_params.get('category_id', None)
        tag = request.query_params.get('tag_id', None)
        user = self.request.query_params.get('user_id', None)

        if category is not None:
            posts = posts.filter(category_id=category)
        if user is not None:
            posts = posts.filter(user_id=user)
        if tag is not None:
            posts = posts.filter(tags=tag)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.create(
            user=user,
            category=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            content=request.data["content"],
            approved=request.data["approved"]
        )
        post.tags.set(request.data["tags"])
        post.reactions.set(request.data["reactions"])

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
        user = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        if user.id != post.user.id and user.user.is_staff == False:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.reactions.set(request.data["reactions"])
        post.tags.set(request.data["tags"])
        
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'reactions')
        depth = 2
