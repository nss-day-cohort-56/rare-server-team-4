from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Comment
from ..models.users import RareUser
from ..models.post import Post

class CommentView(ViewSet):
    """Rare Comment View"""
    def retrieve(self, request, pk):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all().order_by("date")
        comment_post = request.query_params.get('post_id', None)
        if comment_post is not None:
            comments = comments.filter(post_id=comment_post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST request for comment"""

        # Foreign Keys
        post = Post.objects.get(pk=request.data["post_id"]) # Check client's side
        author = RareUser.objects.get(user=request.auth.user)
        
        comment = Comment.objects.create(
            #model    #client
            post_id = post,
            author_id = author,
            subject = request.data["subject"],
            content = request.data["content"],
            date = request.data["date"]
        )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for comment"""

        author = RareUser.objects.get(user=request.auth.user)
        
        comment = Comment.objects.get(pk=pk)
        comment.author_id = author
        comment.content = request.data["content"]
        comment.date = request.data["date"]

        comment.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Comment"""
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'subject', 'author_id', 'post_id', 'content', 'date')
        depth = 2