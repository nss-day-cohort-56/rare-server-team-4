from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Subscription, RareUser
import datetime


class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for authors
    """
    class Meta: 
        model = RareUser
        fields = ('id','user','posts', 'profile_image_url')
        depth = 1
class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions
    """
    author = AuthorSerializer()
    class Meta: 
        model = Subscription
        fields = ('id','subscriber','author','created_at', 'unsubscribed_at', 'is_active')
        depth = 1
        

class SubscriptionView(ViewSet):
    """Rare subscriptions view"""
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized subscription
        """
        
        subscriber = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk=request.data["author"])
        
        subscription = Subscription.objects.create(
            subscriber = subscriber,
            author = author,
            created_at = datetime.datetime.now()
        )
        
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET Requests to get all subscriptions
        Returns:
            Response -- JSON serialized list of subscriptions
        """
        author = request.query_params.get('author', None)

        subscriptions = Subscription.objects.all()
        
        if author is not None:
            subscriptions = subscriptions.filter(author_id=author)
        
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a subscription

        Returns:
            Response -- Empty body with 204 status code
        """

        subscription = Subscription.objects.get(pk=pk)
        subscription.subscriber_id = request.data["subscriber"]
        subscription.author_id = request.data["author"]
        subscription.created_at = request.data["created_at"]        
        subscription.is_active = request.data["is_active"]
        
        if subscription.unsubscribed_at == None:
            subscription.unsubscribed_at = datetime.datetime.now()
        elif subscription.unsubscribed_at != None:
            subscription.unsubscribed_at = None

        subscription.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)