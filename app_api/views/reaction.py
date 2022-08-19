from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.reaction import Reaction


class ReactionView(ViewSet):
    """Reaction View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single reaction
        Returns:
            Response -- JSON serialized reaction"""
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction)
            return Response(serializer.data)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all reactions

        Returns:
            Response -- JSON serialized list of events
        """
        reactions = Reaction.objects.all()
        reaction_post = request.query_params.get('post', None)
        if reaction_post is not None:
            reactions = reactions.filter(post_id=reaction_post)
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response --JSON serialized reaction instance
            """
        if request.auth.user.is_staff:
            reaction = Reaction.objects.create(
                emoji=request.data["emoji"]
            )

            serializer = ReactionSerializer(reaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a reaction
        
        Returns:
            Response -- Empty body with 204 status code
            """
        if request.auth.user.is_staff:
            reaction = Reaction.objects.get(pk=pk)
            reaction.emoji=request.data["emoji"]
            reaction.save()

            return Response(None, status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        if request.auth.user.is_staff:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions"""
    class Meta:
        model = Reaction
        fields = ('id', 'emoji')
