from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import JobSeeker, Company, Location, Industry, JobSeekerPreferences, SkillLevel
from .serializers import (
    UserSerializer, JobSeekerSerializer, CompanySerializer,
    LocationSerializer, IndustrySerializer, JobSeekerPreferencesSerializer,
    UserRegistrationSerializer, SkillLevelSerializer
)
from rest_framework.decorators import api_view

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
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

@api_view(['GET'])
def is_jobseeker(request):
    is_jobseeker = JobSeeker.objects.filter(user=request.user).exists()
    return Response({'is_jobseeker': is_jobseeker})

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

class JobSeekerPreferencesDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerPreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return JobSeekerPreferences.objects.get(job_seeker__user=self.request.user)
