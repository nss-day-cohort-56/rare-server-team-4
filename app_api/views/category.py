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
    
    def list(self, request):
        """Handle GET requests to get all categories
        
        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """Handle PUT requests for a category
        
        Returns: 
            Response -- Empty body with 204 status code
        """
        
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model=Category
        fields=('id', 'label')