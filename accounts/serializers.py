from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    JobSeeker, Company, Location, Industry, Language,
    Certification, Education, Skill, CareerHistory,
    JobSeekerSkill
)

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
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                 'user_type', 'gender', 'phone_number', 'address')
        read_only_fields = ('id',)

class JobSeekerSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerSkill
        fields = '__all__'

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
    languages = LanguageSerializer(many=True, required=False)
    preferred_locations = LocationSerializer(many=True, required=False)
    career_histories = CareerHistorySerializer(many=True, read_only=True, source='careerhistory_set')

    class Meta:
        model = JobSeeker
        fields = '__all__'
        read_only_fields = ('slug',)

    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        certifications_data = validated_data.pop('certifications', [])
        languages_data = validated_data.pop('languages', [])
        preferred_locations_data = validated_data.pop('preferred_locations', [])
        
        job_seeker = JobSeeker.objects.create(**validated_data)
        
        if education_data:
            for edu_data in education_data:
                education = Education.objects.create(**edu_data)
                job_seeker.education.add(education)
            
        if certifications_data:
            for cert_data in certifications_data:
                certification = Certification.objects.create(**cert_data)
                job_seeker.certifications.add(certification)
            
        if languages_data:
            for lang_data in languages_data:
                language = Language.objects.create(**lang_data)
                job_seeker.languages.add(language)

        if preferred_locations_data:
            for loc_data in preferred_locations_data:
                location = Location.objects.create(**loc_data)
                job_seeker.preferred_locations.add(location)
            
        return job_seeker

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'
        read_only_fields = ('slug',)

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    industry = IndustrySerializer()
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