from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, APIException
from .models import (
    JobSeeker, Company, Location, Industry, Language,
    Certification, Education, Skill, CareerHistory
)
from .serializers import (
    UserSerializer, JobSeekerSerializer, CompanySerializer,
    LocationSerializer, IndustrySerializer, LanguageSerializer,
    CertificationSerializer, EducationSerializer, SkillSerializer,
    CareerHistorySerializer,
    UserRegistrationSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class JobSeekerListCreateView(generics.ListCreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobSeekerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class IndustryListCreateView(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class LanguageListCreateView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CertificationListCreateView(generics.ListCreateAPIView):
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get certification records associated with the user's JobSeeker profile
        return Certification.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise ValidationError("You must have a JobSeeker profile to add certification records.")
        
        # Create the certification record
        certification = serializer.save()
        # Add it to the JobSeeker's certifications
        job_seeker.certifications.add(certification)

class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get education records associated with the user's JobSeeker profile
        return Education.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add education records.")
        
        if Education.objects.filter(year_of_completion=serializer.validated_data['year_of_completion']).exists():
            raise APIException("You have already added an education record for this year.")
        
        if Education.objects.filter(course_or_qualification=serializer.validated_data['course_or_qualification']).exists():
            raise APIException("You have already added an education record for this course or qualification.")
        
        # Create the education record
        education = serializer.save()
        # Add it to the JobSeeker's education
        job_seeker.education.add(education)

class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CareerHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get career history records associated with the user's JobSeeker profile
        return CareerHistory.objects.filter(job_seeker__user=self.request.user)
    
    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add career history records.")
        
        # Create the career history record
        career_history = serializer.save()
        # Add it to the JobSeeker's career history
        job_seeker.career_history.add(career_history)



@api_view(['GET'])
def is_jobseeker(request):
    is_jobseeker = JobSeeker.objects.filter(user=request.user).exists()
    return Response({'is_jobseeker': is_jobseeker})

@api_view(['GET'])
def is_company(request):
    is_company = Company.objects.filter(user=request.user).exists()
    return Response({'is_company': is_company})

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Skill.objects.filter(job_seeker__user=self.request.user)
    
    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add skill records.")
        
        # Create the skill record
        skill = serializer.save()
        # Add it to the JobSeeker's skills
        job_seeker.skills.add(skill)


class CareerHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerHistory.objects.all()
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
