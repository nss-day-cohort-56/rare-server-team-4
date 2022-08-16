from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import RareUser


class ProfileView(ViewSet):
    """Rare profiles list view"""

    def list(self, request):
        """Handle GET requests to get all profiles

        Returns:
            Response -- JSON serialized list of profiles
        """
        profiles = RareUser.objects.all()

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single profile
        Returns:
            Response -- JSON serialized profile"""
        try:
            profile = RareUser.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url')
        depth = 1
