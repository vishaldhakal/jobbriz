from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import JobSeeker, Company, Location, Industry, JobSeekerPreferences, SkillLevel

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 
                 'user_type', 'gender', 'phone_number', 'address')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SkillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevel
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skill_levels = SkillLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobSeeker
        fields = '__all__'

class JobSeekerPreferencesSerializer(serializers.ModelSerializer):
    preferred_locations = LocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobSeekerPreferences
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    
    class Meta:
        model = Company
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 
                 'last_name', 'user_type', 'gender', 'phone_number', 'address')

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) 