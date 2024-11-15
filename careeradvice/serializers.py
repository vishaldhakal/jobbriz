from rest_framework import serializers
from .models import CareerPath, CareerTool

class CareerPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPath
        fields = '__all__'

class CareerToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTool
        fields = '__all__'