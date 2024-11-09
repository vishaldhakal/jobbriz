from rest_framework import serializers
from .models import (MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
                    JobPost, JobApplication, SavedJob)
from accounts.serializers import CompanySerializer, LocationSerializer, JobSeekerSerializer

class MajorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorGroup
        fields = ['id', 'code', 'title', 'slug', 'description']

class SubMajorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMajorGroup
        fields = ['id', 'major_group', 'code', 'title', 'slug', 'description']

class MinorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinorGroup
        fields = ['id', 'sub_major_group', 'code', 'title', 'slug', 'description']

class UnitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ['id', 'minor_group', 'code', 'title', 'slug', 'description']

class JobPostListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'slug', 'company', 'required_skill_level',
            'required_education', 'salary_range_min', 'salary_range_max',
            'location', 'is_active', 'posted_date', 'deadline',
            'employment_type'
        ]

class JobPostDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)
    
    class Meta:
        model = JobPost
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = JobSeekerSerializer(read_only=True)
    job = JobPostListSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applied_date', 'updated_at']

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobPostListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ['saved_date'] 