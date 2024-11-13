from django.shortcuts import render, get_object_or_404
from django.db.models import F
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException, ValidationError
from .models import (
    MajorGroup, SubMajorGroup, MinorGroup, UnitGroup,
    JobPost, JobApplication, SavedJob, HireRequest
)
from .serializers import (
    MajorGroupSerializer, SubMajorGroupSerializer,
    MinorGroupSerializer, UnitGroupSerializer,
    JobPostListSerializer, JobPostDetailSerializer,
    JobApplicationSerializer, JobApplicationStatusUpdateSerializer,
    SavedJobSerializer, JobListAllSerializer, HireRequestSerializer,
    HireRequestStatusUpdateSerializer
)
from accounts.models import Company, JobSeeker
from django.db import models
from django.utils import timezone


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

class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class JobPostListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        queryset = self.get_queryset()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = JobListAllSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        queryset = JobPost.objects.filter(status='Published')
        
        # Keyword search
        keywords = self.request.query_params.get('keywords')
        if keywords:
            queryset = queryset.filter(
                models.Q(title__icontains=keywords) |
                models.Q(description__icontains=keywords) |
                models.Q(requirements__icontains=keywords)
            )
        
        # Classification (Unit Group) filter
        classification = self.request.query_params.get('classification')
        if classification:
            queryset = queryset.filter(unit_group__slug=classification)
            
        # Location filter
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__name__icontains=location)
            
        # Employment type filter
        work_type = self.request.query_params.get('work_type')
        if work_type and work_type != 'Any work type':
            queryset = queryset.filter(employment_type=work_type)
            
        # Salary range filter
        salary_min = self.request.query_params.get('salary_min')
        salary_max = self.request.query_params.get('salary_max')
        if salary_min:
            queryset = queryset.filter(salary_range_min__gte=salary_min)
        if salary_max:
            queryset = queryset.filter(salary_range_max__lte=salary_max)
            
        # Posted date filter
        listing_time = self.request.query_params.get('listing_time')
        if listing_time:
            if listing_time == 'Last 24 hours':
                date_threshold = timezone.now() - timezone.timedelta(days=1)
            elif listing_time == 'Last 3 days':
                date_threshold = timezone.now() - timezone.timedelta(days=3)
            elif listing_time == 'Last 7 days':
                date_threshold = timezone.now() - timezone.timedelta(days=7)
            elif listing_time == 'Last 14 days':
                date_threshold = timezone.now() - timezone.timedelta(days=14)
            elif listing_time == 'Last 30 days':
                date_threshold = timezone.now() - timezone.timedelta(days=30)
            
            if date_threshold:
                queryset = queryset.filter(posted_date__gte=date_threshold)
        
        return queryset.order_by('-posted_date')

    def perform_create(self, serializer):
        if self.request.user.user_type != 'Employer':
            raise APIException("Only company users can create job posts")
        company = Company.objects.get(user=self.request.user)
        unit_group = UnitGroup.objects.get(code=self.request.data.get('unit_group'))
        serializer.save(company=company, unit_group=unit_group)

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
    serializer_class = JobListAllSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        company = Company.objects.get(user=self.request.user)
        queryset = JobPost.objects.filter(company=company)
        
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

        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by skill level
        skill_level = self.request.query_params.get('skill_level')
        if skill_level:
            queryset = queryset.filter(required_skill_level=skill_level)
            
        return queryset


class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.user_type != 'Job Seeker':
            raise ValidationError("Only job seekers can apply for jobs")
        
        job_slug = self.kwargs.get('job_slug')
        job = get_object_or_404(JobPost, slug=job_slug)
        
        if JobApplication.objects.filter(job=job, applicant=self.request.user.jobseeker).exists():
            raise ValidationError("You have already applied for this job")
        job_seeker = JobSeeker.objects.get(user=self.request.user)
        serializer.save(
            applicant=job_seeker,
            job=job
        )

class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Job Seeker':
            return JobApplication.objects.filter(applicant=user.jobseeker)
        elif user.user_type == 'Employer':
            company = Company.objects.get(user=user)
            job_applications = JobApplication.objects.filter(job__company=company)
            job_slug = self.request.query_params.get('job_slug')
            if job_slug:
                job_post = JobPost.objects.get(slug=job_slug)
                job_applications = job_applications.filter(job=job_post)
            return job_applications
        return JobApplication.objects.none()

class JobApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Job Seeker':
            job_seeker = JobSeeker.objects.get(user=user)
            return JobApplication.objects.filter(applicant=job_seeker)
        elif user.user_type == 'Employer':
            company = Company.objects.get(user=user)
            return JobApplication.objects.filter(job__company=company)
        return JobApplication.objects.none()

class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = JobApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Employer':
            company = Company.objects.get(user=user)
            return JobApplication.objects.filter(job__company=company)
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

class HireRequestCreateView(generics.CreateAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'Employer':
            raise ValidationError("Only employers can create hire requests")
            
        job_slug = self.kwargs.get('job_slug')
        jobseeker_slug = self.kwargs.get('jobseeker_slug')
        
        job = get_object_or_404(JobPost, slug=job_slug)
        job_seeker = get_object_or_404(JobSeeker, slug=jobseeker_slug)
        
        if HireRequest.objects.filter(job=job, job_seeker=job_seeker).exists():
            raise ValidationError("A hire request already exists for this job seeker")
            
        serializer.save(
            job=job,
            job_seeker=job_seeker
        )

class HireRequestListView(generics.ListAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Employer':
            company = Company.objects.get(user=user)
            return HireRequest.objects.filter(job__company=company)
        elif user.user_type == 'Job Seeker':
            job_seeker = JobSeeker.objects.get(user=user)
            return HireRequest.objects.filter(job_seeker=job_seeker)
        return HireRequest.objects.none()

class HireRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HireRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Employer':
            company = Company.objects.get(user=user)
            return HireRequest.objects.filter(job__company=company)
        elif user.user_type == 'Job Seeker':
            job_seeker = JobSeeker.objects.get(user=user)
            return HireRequest.objects.filter(job_seeker=job_seeker)
        return HireRequest.objects.none()

class HireRequestStatusUpdateView(generics.UpdateAPIView):
    serializer_class = HireRequestStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'Job Seeker':
            job_seeker = JobSeeker.objects.get(user=user)
            return HireRequest.objects.filter(job_seeker=job_seeker)
        return HireRequest.objects.none()