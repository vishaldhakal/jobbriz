from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    JobSeeker, Company, Location, Industry, Language,
    Certification, Education, Skill, CareerHistory
)
from job.models import UnitGroup, HireRequest

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                 'user_type', 'gender', 'phone_number', 'address')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    jobseeker_data = serializers.SerializerMethodField()
    company_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'user_type', 'gender', 'phone_number', 'address',
                 'jobseeker_data', 'company_data')
        read_only_fields = ('id',)

    def get_jobseeker_data(self, obj):
        try:
            jobseeker = obj.jobseeker
            return {
                'slug': jobseeker.slug,
            }
        except JobSeeker.DoesNotExist:
            return None

    def get_company_data(self, obj):
        try:
            company = obj.company_profile
            return {
                'slug': company.slug,
            }
        except Company.DoesNotExist:
            return None


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('slug',)

class CareerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerHistory
        fields = '__all__'

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    education = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    languages = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Language.objects.all(),
        required=False
    )
    skills = SkillSerializer(many=True, required=False)
    preferred_locations = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Location.objects.all(),
        required=False
    )
    preferred_unit_groups = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=UnitGroup.objects.all(),
        required=False
    )
    career_histories = CareerHistorySerializer(many=True, required=False)

    class Meta:
        model = JobSeeker
        fields = '__all__'
        read_only_fields = ('slug',)
        depth = 2

    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        certifications_data = validated_data.pop('certifications', [])
        career_histories_data = validated_data.pop('career_histories', [])
        
        job_seeker = JobSeeker.objects.create(**validated_data)
        
        if education_data:
            for edu_data in education_data:
                education = Education.objects.create(**edu_data)
                job_seeker.education.add(education)
            
        if certifications_data:
            for cert_data in certifications_data:
                certification = Certification.objects.create(**cert_data)
                job_seeker.certifications.add(certification)
        
        if career_histories_data:
            for career_history_data in career_histories_data:
                career_history = CareerHistory.objects.create(**career_history_data)
                job_seeker.career_history.add(career_history)
            
        return job_seeker


class JobSeekerSerializer2(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    education = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    preferred_locations = LocationSerializer(many=True, required=False)
    career_histories = CareerHistorySerializer(many=True, required=False)
    already_hired = serializers.SerializerMethodField()

    def get_already_hired(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.user_type == 'Employer':
            try:
                company = Company.objects.get(user=request.user)
                return HireRequest.objects.filter(job__company=company, job_seeker=obj).exists()
            except Company.DoesNotExist:
                return False
        return False

    class Meta:
        model = JobSeeker
        fields = '__all__'
        read_only_fields = ('slug',)
        depth = 2

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ('slug',)

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    logo = serializers.FileField(required=False)
    company_registration_certificate = serializers.FileField(required=False)
    established_date = serializers.DateField(required=False)
    website = serializers.URLField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('slug', 'is_verified')

    def create(self, validated_data):
        industry_data = validated_data.pop('industry')
        industry = Industry.objects.get_or_create(**industry_data)[0]
        company = Company.objects.create(industry=industry, **validated_data)
        return company