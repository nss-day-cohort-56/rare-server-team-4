from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Subscription, RareUser

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions
    """
    class Meta: 
        model = Subscription
        fields = ('id','subscriber','author','created_at')
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
            author = author
        )
        
        if subscription.subscriber == subscription.author:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        
        if Subscription.objects.filter(subscriber = subscription.subscriber, author = subscription.author).exists():
            return Response(None, status=status.HTTP_403_FORBIDDEN)
            
        
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET Requests to get all subscriptions
        Returns:
            Response -- JSON serialized list of subscriptions
        """
        
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)