from rest_framework import generics
from .models import CareerPath, CareerTool
from .serializers import CareerPathSerializer, CareerToolSerializer

class CareerPathListView(generics.ListAPIView):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    filterset_fields = ['title']
    search_fields = ['title', 'description']

class CareerToolListView(generics.ListAPIView):
    queryset = CareerTool.objects.filter(is_active=True)
    serializer_class = CareerToolSerializer
    filterset_fields = ['tool_type']