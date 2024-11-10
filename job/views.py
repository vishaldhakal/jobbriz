from django.shortcuts import render, get_object_or_404
from django.db.models import F
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import (
    MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
    JobPost, JobApplication, SavedJob
)
from .serializers import (
    MajorGroupSerializer, SubMajorGroupSerializer,
    MinorGroupSerializer, UnitGroupSerializer,
    JobPostListSerializer, JobPostDetailSerializer,
    JobApplicationSerializer, JobApplicationStatusUpdateSerializer,
    SavedJobSerializer
)

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

class SubMajorGroupListCreateView(generics.ListCreateAPIView):
    queryset = SubMajorGroup.objects.all()
    serializer_class = SubMajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubMajorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubMajorGroup.objects.all()
    serializer_class = SubMajorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class MinorGroupListCreateView(generics.ListCreateAPIView):
    queryset = MinorGroup.objects.all()
    serializer_class = MinorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MinorGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MinorGroup.objects.all()
    serializer_class = MinorGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class UnitGroupListCreateView(generics.ListCreateAPIView):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UnitGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class JobPostListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = JobPost.objects.filter(status='Published')
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__slug=location)
            
        # Filter by employment type
        employment_type = self.request.query_params.get('employment_type')
        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)
            
        # Filter by education
        education = self.request.query_params.get('education')
        if education:
            queryset = queryset.filter(required_education=education)
            
        # Filter by skill level
        skill_level = self.request.query_params.get('skill_level')
        if skill_level:
            queryset = queryset.filter(required_skill_level=skill_level)
            
        return queryset

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'company'):
            raise ValidationError("Only company users can create job posts")
        serializer.save(company=self.request.user.company)

class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class JobPostViewCountView(views.APIView):
    def post(self, request, slug):
        job_post = get_object_or_404(JobPost, slug=slug)
        job_post.views_count = F('views_count') + 1
        job_post.save()
        return Response(status=status.HTTP_200_OK)

class CompanyJobListView(generics.ListAPIView):
    serializer_class = JobPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        company_slug = self.kwargs.get('company_slug')
        return JobPost.objects.filter(
            company__slug=company_slug,
            status='Published'
        )

class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'jobseeker'):
            raise ValidationError("Only job seekers can apply for jobs")
        
        job_slug = self.kwargs.get('job_slug')
        job = get_object_or_404(JobPost, slug=job_slug)
        
        if JobApplication.objects.filter(job=job, applicant=self.request.user.jobseeker).exists():
            raise ValidationError("You have already applied for this job")
            
        serializer.save(
            applicant=self.request.user.jobseeker,
            job=job
        )

class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'jobseeker'):
            return JobApplication.objects.filter(applicant=user.jobseeker)
        elif hasattr(user, 'company'):
            return JobApplication.objects.filter(job__company=user.company)
        return JobApplication.objects.none()

class JobApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'jobseeker'):
            return JobApplication.objects.filter(applicant=user.jobseeker)
        elif hasattr(user, 'company'):
            return JobApplication.objects.filter(job__company=user.company)
        return JobApplication.objects.none()

class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = JobApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'company'):
            return JobApplication.objects.filter(job__company=self.request.user.company)
        return JobApplication.objects.none()

class SavedJobToggleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_slug):
        if not hasattr(request.user, 'jobseeker'):
            raise ValidationError("Only job seekers can save jobs")
            
        job = get_object_or_404(JobPost, slug=job_slug)
        saved_job, created = SavedJob.objects.get_or_create(
            job_seeker=request.user.jobseeker,
            job=job
        )
        
        if not created:
            saved_job.delete()
            return Response({"status": "removed"}, status=status.HTTP_200_OK)
            
        return Response({"status": "saved"}, status=status.HTTP_201_CREATED)

class SavedJobListView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'jobseeker'):
            return SavedJob.objects.filter(job_seeker=self.request.user.jobseeker)
        return SavedJob.objects.none()