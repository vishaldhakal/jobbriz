from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import (MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
                    JobPost, JobApplication, SavedJob)
from .serializers import (MajorGroupSerializer, SubMajorGroupSerializer,
                         MinorGroupSerializer, UnitGroupSerializer,
                         JobPostListSerializer, JobPostDetailSerializer,
                         JobApplicationSerializer, SavedJobSerializer)

# Create your views here.

class MajorGroupListCreateView(generics.ListCreateAPIView):
    queryset = MajorGroup.objects.all()
    serializer_class = MajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MajorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MajorGroup.objects.all()
    serializer_class = MajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

# Similar views for SubMajorGroup, MinorGroup, and UnitGroup...

class JobPostListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = JobPost.objects.filter(is_active=True)
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__slug=location)
        return queryset

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class JobApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'jobseeker'):
            return JobApplication.objects.filter(applicant=self.request.user.jobseeker)
        return JobApplication.objects.none()

    def perform_create(self, serializer):
        job_id = self.kwargs.get('job_id')
        job = JobPost.objects.get(id=job_id)
        serializer.save(applicant=self.request.user.jobseeker, job=job)

class SavedJobListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'jobseeker'):
            return SavedJob.objects.filter(job_seeker=self.request.user.jobseeker)
        return SavedJob.objects.none()

    def perform_create(self, serializer):
        job_id = self.kwargs.get('job_id')
        job = JobPost.objects.get(id=job_id)
        serializer.save(job_seeker=self.request.user.jobseeker, job=job)
