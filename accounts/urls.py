from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserDetailView, JobSeekerListCreateView, JobSeekerDetailView,
    CompanyListCreateView, CompanyDetailView, LocationListCreateView,
    IndustryListCreateView, LanguageListCreateView, CertificationListCreateView,
    EducationListCreateView, CareerHistoryListCreateView, JobSeekerSkillListCreateView,
    is_jobseeker, is_company
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
    
    # Location URLs
    path('locations/', LocationListCreateView.as_view(), name='location-list'),
    
    # Industry URLs
    path('industries/', IndustryListCreateView.as_view(), name='industry-list'),
    
    # Additional Model URLs
    path('languages/', LanguageListCreateView.as_view(), name='language-list'),
    path('certifications/', CertificationListCreateView.as_view(), name='certification-list'),
    path('education/', EducationListCreateView.as_view(), name='education-list'),
    path('career-history/', CareerHistoryListCreateView.as_view(), name='career-history-list'),
    path('jobseeker-skills/', JobSeekerSkillListCreateView.as_view(), name='jobseeker-skill-list'),
] 