from rest_framework import serializers
from .models import (MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
                    JobPost, JobApplication, SavedJob)
from accounts.serializers import CompanySerializer, LocationSerializer, JobSeekerSerializer

class MajorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorGroup
        fields = ['id', 'code', 'title', 'slug', 'description']

class SubMajorGroupSerializer(serializers.ModelSerializer):
    major_group = MajorGroupSerializer(read_only=True)
    
    class Meta:
        model = SubMajorGroup
        fields = ['id', 'major_group', 'code', 'title', 'slug', 'description']

class MinorGroupSerializer(serializers.ModelSerializer):
    sub_major_group = SubMajorGroupSerializer(read_only=True)
    
    class Meta:
        model = MinorGroup
        fields = ['id', 'sub_major_group', 'code', 'title', 'slug', 'description']

class UnitGroupSerializer(serializers.ModelSerializer):
    minor_group = MinorGroupSerializer(read_only=True)
    
    class Meta:
        model = UnitGroup
        fields = ['id', 'minor_group', 'code', 'title', 'slug', 'description']

class JobPostListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'slug', 'company', 'required_skill_level',
            'required_education', 'salary_range_min', 'salary_range_max',
            'location', 'status', 'posted_date', 'deadline',
            'employment_type', 'applications_count', 'views_count',
            'show_salary'
        ]

class JobPostDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = JobPost
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = JobSeekerSerializer(read_only=True)
    job = JobPostListSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applied_date', 'updated_at', 'status']

class JobApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobPostListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ['saved_date'] 