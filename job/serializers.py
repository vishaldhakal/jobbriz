from rest_framework import serializers
from .models import (MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
                    JobPost, JobApplication, SavedJob, HireRequest)
from accounts.serializers import CompanySerializer, LocationSerializer, JobSeekerSerializer
from accounts.models import Company, Location, JobSeeker
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

class JobPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating job posts"""
    location = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Location.objects.all(),
        required=False
    )
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )
    unit_group = serializers.PrimaryKeyRelatedField(
        queryset=UnitGroup.objects.all()
    )

    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ['slug', 'views_count', 'applications_count']

class CompanySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'slug','logo','industry']

class UnitGroupSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ['id', 'code', 'title', 'slug','minor_group']
        depth = 4

class LocationSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'slug']

class JobListAllSerializer(serializers.ModelSerializer):
    location = LocationSmallSerializer(many=True, read_only=True)
    company = CompanySmallSerializer(read_only=True)
    unit_group = UnitGroupSmallSerializer(read_only=True)
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'slug','location', 'status', 'posted_date', 'deadline', 'employment_type', 'applications_count', 'views_count','company','salary_range_min','salary_range_max','show_salary','unit_group']
        depth = 2

class JobPostListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Location.objects.all(),
        required=False
    )
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)

    
    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'slug', 'company', 'required_skill_level',
            'required_education', 'salary_range_min', 'salary_range_max',
            'location', 'status', 'posted_date', 'deadline',
            'employment_type', 'applications_count', 'views_count',
            'show_salary','description','responsibilities','requirements',
            'unit_group'
        ]
        read_only_fields = ['slug', 'views_count', 'applications_count']

class JobPostDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    unit_group = UnitGroupSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    has_already_applied = serializers.SerializerMethodField()
    
    def get_has_already_applied(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                job_seeker = JobSeeker.objects.get(user=request.user)
                return JobApplication.objects.filter(job=obj, applicant=job_seeker).exists()
            except JobSeeker.DoesNotExist:
                return False
        return False
    
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ['slug', 'views_count', 'applications_count']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications"""
    class Meta:
        model = JobApplication
        fields = ['job', 'cover_letter']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['applicant'] = request.user.jobseeker
        return super().create(validated_data)

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

class SavedJobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating saved jobs"""
    class Meta:
        model = SavedJob
        fields = ['job']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['job_seeker'] = request.user.jobseeker
        return super().create(validated_data)

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobPostListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ['saved_date']

class HireRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = ['status']
        
class HireRequestSerializer(serializers.ModelSerializer):
    job = JobListAllSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)

    class Meta:
        model = HireRequest
        fields = ['id', 'job', 'job_seeker', 'requested_date', 'status','message']
        read_only_fields = ['requested_date']