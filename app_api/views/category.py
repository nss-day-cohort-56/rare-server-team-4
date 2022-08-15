from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Category

class CategoryView(ViewSet):
    """rare category view"""
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized game instance
        """
        category = Category.objects.create(
            label = request.data["label"]
        )
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model=Category
        fields=('id', 'label')