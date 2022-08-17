from argparse import Action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import RareUser
from django.contrib.auth.models import User
from rest_framework.decorators import action


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

    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """
        # currentUser = RareUser.objects.get(user=request.auth.user)
        # if currentUser.user.is_staff is not True:
        #     return Response(None, status=status.HTTP_401_UNAUTHORIZED)
    @action(methods=['PUT'], detail=True)
    def user_active(self, request, pk):
        user = User.objects.get(pk=pk) #django
        user.is_active = not user.is_active
        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url')
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')