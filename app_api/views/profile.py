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


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url')
        depth = 1
