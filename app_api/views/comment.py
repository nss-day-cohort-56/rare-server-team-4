from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Comment
from ..models.users import RareUser
from ..models.post import Post
import datetime

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
        comments = Comment.objects.all().order_by("created_on")
        post = request.query_params.get('post_id', None)
        if post is not None:
            comments = comments.filter(post_id=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST request for comment"""

        # Foreign Keys
        post = Post.objects.get(pk=request.data["post_id"]) # Check client's side
        author = RareUser.objects.get(user=request.auth.user)
        
        comment = Comment.objects.create(
            #model    #client
            post = post,
            author = author,
            subject = request.data["subject"],
            content = request.data["content"],
            created_on = datetime.date.today()
        )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for comment"""

        author = RareUser.objects.get(user=request.auth.user)
        
        comment = Comment.objects.get(pk=pk)
        comment.author = author
        
        comment.content = request.data["content"]
        comment.subject = request.data["subject"]

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
        fields = ('id', 'subject', 'author', 'post', 'content', 'created_on')
        depth = 2