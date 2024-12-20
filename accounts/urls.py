from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserDetailView, JobSeekerListCreateView, JobSeekerDetailView,
    CompanyListCreateView, CompanyDetailView, LocationListCreateView,
    IndustryListCreateView, LanguageListCreateView, CertificationListCreateView,
    EducationListCreateView, CareerHistoryListCreateView,
    is_jobseeker, is_company, EducationDetailView, SkillListCreateView,
    SkillDetailView, CertificationDetailView, CareerHistoryDetailView,
    FeaturedCompanyListView, CompanyListView
)

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User URLs
    path('user/profile/', UserDetailView.as_view(), name='user-detail'),
    
    # JobSeeker URLs
    path('is-jobseeker/', is_jobseeker, name='is-jobseeker'),
    path('jobseekers/', JobSeekerListCreateView.as_view(), name='jobseeker-list'),
    path('jobseekers/<slug:slug>/', JobSeekerDetailView.as_view(), name='jobseeker-detail'),
    
    # Company URLs
    path('is-company/', is_company, name='is-company'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<slug:slug>/', CompanyDetailView.as_view(), name='company-detail'),
    path('companies-list/', CompanyListView.as_view(), name='companies-list'),
    
    # Location URLs
    path('locations/', LocationListCreateView.as_view(), name='location-list'),
    
    # Industry URLs
    path('industries/', IndustryListCreateView.as_view(), name='industry-list'),
    
    # Additional Model URLs
    path('languages/', LanguageListCreateView.as_view(), name='language-list'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('certifications/', CertificationListCreateView.as_view(), name='certification-list'),
    path('certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
    path('education/', EducationListCreateView.as_view(), name='education-list'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
    path('career-history/', CareerHistoryListCreateView.as_view(), name='career-history-list'),
    path('career-history/<int:pk>/', CareerHistoryDetailView.as_view(), name='career-history-detail'),
    path('featured-companies/', FeaturedCompanyListView.as_view(), name='featured-companies'),
] 