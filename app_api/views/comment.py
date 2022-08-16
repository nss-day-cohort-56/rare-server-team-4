from dataclasses import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Comment

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
        comments = Comment.objects.all()
        comment_post = request.query_params.get('post_id', None)
        if comment_post is not None:
            comments = comments.filter(post_id=comment_post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'subject', 'author_id', 'post_id', 'content', 'date')
        depth = 2