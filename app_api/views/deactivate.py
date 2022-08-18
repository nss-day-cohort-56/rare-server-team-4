from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Deactivate
from app_api.models import RareUser


class DeactivateView(ViewSet):
    """post view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            deactivate = Deactivate.objects.get(pk=pk)
            serializer = DeactivateSerializer(deactivate)
            return Response(serializer.data)
        except Deactivate.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of events
        """
        deactivates = Deactivate.objects.all()
        deactivatedUser = request.query_params.get('deactivatedUser', None)
        if deactivatedUser is not None:
            deactivates = deactivates.filter(deactivatedUser=deactivatedUser)
        serializer = DeactivateSerializer(deactivates, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)

        deactivate = Deactivate.objects.create(
            deactivatedUser=RareUser.objects.get(pk=request.data["deactivatedUser"]),
            approveUser=user
        )

        serializer = DeactivateSerializer(deactivate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        user = RareUser.objects.get(user=request.auth.user)

        deactivate = Deactivate.objects.get(pk=pk)
        if user.id == deactivate.approveUser:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        deactivate.secondApproveUser = user
        deactivate.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class DeactivateSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    
    class Meta:
        model = Deactivate
        fields = ('id', 'deactivatedUser', 'approveUser', 'secondApproveUser')
        depth = 2