from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import (
    JobSeeker, Company, Location, Industry, Language,
    Certification, Education, Skill, CareerHistory,
    JobSeekerSkill
)
from .serializers import (
    UserSerializer, JobSeekerSerializer, CompanySerializer,
    LocationSerializer, IndustrySerializer, LanguageSerializer,
    CertificationSerializer, EducationSerializer, SkillSerializer,
    CareerHistorySerializer, JobSeekerSkillSerializer,
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
    permission_classes = (permissions.IsAuthenticated,)

class IndustryListCreateView(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = (permissions.IsAuthenticated,)

class LanguageListCreateView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CertificationListCreateView(generics.ListCreateAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CareerHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CareerHistory.objects.filter(job_seeker__user=self.request.user)

    def perform_create(self, serializer):
        job_seeker = get_object_or_404(JobSeeker, user=self.request.user)
        serializer.save(job_seeker=job_seeker)

class JobSeekerSkillListCreateView(generics.ListCreateAPIView):
    queryset = JobSeekerSkill.objects.all()
    serializer_class = JobSeekerSkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

@api_view(['GET'])
def is_jobseeker(request):
    is_jobseeker = JobSeeker.objects.filter(user=request.user).exists()
    return Response({'is_jobseeker': is_jobseeker})

@api_view(['GET'])
def is_company(request):
    is_company = Company.objects.filter(user=request.user).exists()
    return Response({'is_company': is_company})
