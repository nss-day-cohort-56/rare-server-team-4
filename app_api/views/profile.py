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

    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """

        user = RareUser.objects.get(pk=pk)
        if user.user.is_staff is not true:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        user.user.is_active = request.data["user.is_active"]
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url')
        depth = 1
